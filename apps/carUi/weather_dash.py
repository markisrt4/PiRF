import math
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

import requests
import streamlit as st
import geocoder
from streamlit_autorefresh import st_autorefresh

# Optional GPSD support
try:
    import gpsd
    GPSD_AVAILABLE = True
except ImportError:
    GPSD_AVAILABLE = False


# -----------------------------
# Configuration
# -----------------------------
REFRESH_SECONDS = 60
USE_GPSD = True              # True if you want to try real GPS first
GPSD_HOST = "127.0.0.1"
GPSD_PORT = 2947

# If location lookup fails, fall back here
DEFAULT_LAT = 40.7128
DEFAULT_LON = -74.0060
DEFAULT_LOCATION_NAME = "Fallback Location"


# -----------------------------
# Streamlit setup
# -----------------------------
st.set_page_config(page_title="Car Weather", layout="wide")

st.markdown("""
<style>
    .main {
        background-color: #0f1116;
        color: white;
    }
    .metric-card {
        background-color: #1b1f2a;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #2a3142;
    }
    .small-muted {
        color: #aab4c5;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Auto-refresh the app
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="weather_refresh")

st.title("🚗 Live Car Weather")


# -----------------------------
# Weather code mapping
# -----------------------------
WMO_CODES = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear",
    2: "⛅ Partly cloudy",
    3: "☁️ Overcast",
    45: "🌫️ Fog",
    48: "🌫️ Rime fog",
    51: "🌦️ Light drizzle",
    53: "🌦️ Moderate drizzle",
    55: "🌦️ Dense drizzle",
    56: "🌧️ Freezing drizzle",
    57: "🌧️ Dense freezing drizzle",
    61: "🌧️ Slight rain",
    63: "🌧️ Moderate rain",
    65: "🌧️ Heavy rain",
    66: "🌧️ Freezing rain",
    67: "🌧️ Heavy freezing rain",
    71: "🌨️ Slight snow",
    73: "🌨️ Moderate snow",
    75: "❄️ Heavy snow",
    77: "🌨️ Snow grains",
    80: "🌦️ Slight rain showers",
    81: "🌦️ Moderate rain showers",
    82: "⛈️ Violent rain showers",
    85: "🌨️ Slight snow showers",
    86: "🌨️ Heavy snow showers",
    95: "⛈️ Thunderstorm",
    96: "⛈️ Thunderstorm w/ hail",
    99: "⛈️ Severe thunderstorm w/ hail",
}


# -----------------------------
# Helpers
# -----------------------------
def wind_dir_from_degrees(deg: Optional[float]) -> str:
    if deg is None:
        return "N/A"
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = round(deg / 45) % 8
    return directions[idx]


def c_to_f(c: Optional[float]) -> str:
    if c is None:
        return "N/A"
    return f"{(c * 9/5) + 32:.1f}°F"


def kmh_to_mph(kmh: Optional[float]) -> str:
    if kmh is None:
        return "N/A"
    return f"{kmh * 0.621371:.1f} mph"


@st.cache_data(ttl=45)
def get_ip_location() -> Dict[str, Any]:
    g = geocoder.ip("me")
    if g.ok and g.latlng:
        city = g.city or ""
        state = g.state or ""
        country = g.country or ""
        name = ", ".join(part for part in [city, state, country] if part)
        return {
            "lat": g.latlng[0],
            "lon": g.latlng[1],
            "name": name or "IP-based location",
            "source": "IP geolocation",
        }
    raise RuntimeError("IP geolocation failed")


def get_gpsd_location() -> Dict[str, Any]:
    if not GPSD_AVAILABLE:
        raise RuntimeError("gpsd-py3 not installed")

    gpsd.connect(host=GPSD_HOST, port=GPSD_PORT)
    packet = gpsd.get_current()

    if packet.mode < 2:
        raise RuntimeError("GPS fix not available")

    lat = packet.lat
    lon = packet.lon

    if lat is None or lon is None:
        raise RuntimeError("GPS returned no coordinates")

    return {
        "lat": lat,
        "lon": lon,
        "name": f"{lat:.5f}, {lon:.5f}",
        "source": "GPSD",
    }


def get_location() -> Dict[str, Any]:
    # Try real GPS first
    if USE_GPSD:
        try:
            return get_gpsd_location()
        except Exception as e:
            st.warning(f"GPSD lookup failed, falling back to IP location: {e}")

    # Fallback to IP-based location
    try:
        return get_ip_location()
    except Exception as e:
        st.warning(f"IP location failed, using default coordinates: {e}")
        return {
            "lat": DEFAULT_LAT,
            "lon": DEFAULT_LON,
            "name": DEFAULT_LOCATION_NAME,
            "source": "Static fallback",
        }


@st.cache_data(ttl=300)
def reverse_geocode(lat: float, lon: float) -> str:
    try:
        g = geocoder.osm([lat, lon], method="reverse")
        if g.ok:
            city = g.city or g.town or g.village or ""
            state = g.state or ""
            country = g.country or ""
            return ", ".join(part for part in [city, state, country] if part) or f"{lat:.5f}, {lon:.5f}"
    except Exception:
        pass
    return f"{lat:.5f}, {lon:.5f}"


@st.cache_data(ttl=120)
def fetch_weather(lat: float, lon: float) -> Dict[str, Any]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto",
        "current": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "is_day",
            "precipitation",
            "rain",
            "showers",
            "snowfall",
            "weather_code",
            "cloud_cover",
            "pressure_msl",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ]),
        "hourly": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "weather_code",
            "cloud_cover",
            "wind_speed_10m",
        ]),
        "daily": ",".join([
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "sunrise",
            "sunset",
            "precipitation_probability_max",
        ]),
        "forecast_days": 3,
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# -----------------------------
# Main app
# -----------------------------
try:
    loc = get_location()
    lat = loc["lat"]
    lon = loc["lon"]
    pretty_location = reverse_geocode(lat, lon)
    weather = fetch_weather(lat, lon)

    current = weather["current"]
    hourly = weather["hourly"]
    daily = weather["daily"]

    current_code = current.get("weather_code")
    condition = WMO_CODES.get(current_code, f"Unknown ({current_code})")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    wind_dir = wind_dir_from_degrees(current.get("wind_direction_10m"))

    st.caption(
        f"Last updated: {now_str} | Location source: {loc['source']} | Refresh: every {REFRESH_SECONDS}s"
    )

    st.info(f"📍 Location: {pretty_location}  |  Lat/Lon: {lat:.5f}, {lon:.5f}")

    # Current conditions
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Temperature", c_to_f(current.get("temperature_2m")))
        st.metric("Feels Like", c_to_f(current.get("apparent_temperature")))

    with c2:
        st.metric("Condition", condition)
        st.metric("Humidity", f"{current.get('relative_humidity_2m', 'N/A')}%")

    with c3:
        st.metric("Wind", kmh_to_mph(current.get("wind_speed_10m")))
        st.metric("Wind Dir", wind_dir)

    with c4:
        st.metric("Gusts", kmh_to_mph(current.get("wind_gusts_10m")))
        st.metric("Cloud Cover", f"{current.get('cloud_cover', 'N/A')}%")

    # Extra detail row
    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric("Pressure (MSL)", f"{current.get('pressure_msl', 'N/A')} hPa")
    with d2:
        st.metric("Surface Pressure", f"{current.get('surface_pressure', 'N/A')} hPa")
    with d3:
        st.metric("Precipitation Now", f"{current.get('precipitation', 0)} mm")
    with d4:
        st.metric("Rain Now", f"{current.get('rain', 0)} mm")

    # Sunrise / sunset
    st.subheader("Sun")
    s1, s2 = st.columns(2)
    with s1:
        st.metric("Sunrise", daily["sunrise"][0].split("T")[1])
    with s2:
        st.metric("Sunset", daily["sunset"][0].split("T")[1])

    # Next hour precipitation probability
    st.subheader("Near-Term Outlook")

    current_hour = datetime.now().hour
    precip_prob = "N/A"
    if current_hour < len(hourly["precipitation_probability"]):
        precip_prob = f"{hourly['precipitation_probability'][current_hour]}%"

    n1, n2, n3 = st.columns(3)
    with n1:
        st.metric("Rain Chance (This Hour)", precip_prob)
    with n2:
        st.metric("Hourly Precip", f"{hourly['precipitation'][current_hour]} mm")
    with n3:
        next_code = hourly["weather_code"][current_hour]
        st.metric("Hourly Condition", WMO_CODES.get(next_code, f"Code {next_code}"))

    # 24-hour charts
    st.subheader("Next 24 Hours")

    hours = hourly["time"][:24]
    hour_labels = [t.split("T")[1][:5] for t in hours]

    chart_data = {
        "Time": hour_labels,
        "Temp °F": [round((c * 9/5) + 32, 1) for c in hourly["temperature_2m"][:24]],
        "Feels Like °F": [round((c * 9/5) + 32, 1) for c in hourly["apparent_temperature"][:24]],
        "Rain %": hourly["precipitation_probability"][:24],
        "Cloud %": hourly["cloud_cover"][:24],
        "Wind mph": [round(v * 0.621371, 1) for v in hourly["wind_speed_10m"][:24]],
    }

    st.line_chart(chart_data, x="Time", y=["Temp °F", "Feels Like °F"])
    st.line_chart(chart_data, x="Time", y=["Rain %", "Cloud %"])
    st.line_chart(chart_data, x="Time", y=["Wind mph"])

    # Daily outlook
    st.subheader("3-Day Forecast")

    daily_rows = []
    for i in range(len(daily["time"])):
        daily_rows.append({
            "Date": daily["time"][i],
            "Condition": WMO_CODES.get(daily["weather_code"][i], f"Code {daily['weather_code'][i]}"),
            "High": f"{(daily['temperature_2m_max'][i] * 9/5) + 32:.1f}°F",
            "Low": f"{(daily['temperature_2m_min'][i] * 9/5) + 32:.1f}°F",
            "Rain Chance": f"{daily['precipitation_probability_max'][i]}%",
            "Sunrise": daily["sunrise"][i].split("T")[1],
            "Sunset": daily["sunset"][i].split("T")[1],
        })

    st.dataframe(daily_rows, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error fetching weather data: {e}")