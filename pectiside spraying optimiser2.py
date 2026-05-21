import streamlit as st
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Page Configuration (Website ki details)
st.set_page_config(page_title="Pesticide Spraying Optimizer", layout="wide")

# App Header
st.title("🌱 Drone Imagery - Pesticide Spraying Optimizer")
st.write("Upload drone field imagery to detect infection hotspots and optimize chemical usage.")
st.markdown("---")

# Sidebar for settings
st.sidebar.header("⚙️ Optimization Settings")
threshold = st.sidebar.slider("Infection Sensitivity Threshold", min_value=0.0, max_value=0.5, value=0.15, step=0.01)
st.sidebar.info("Tip: Threshold badhane se halka stress bhi 'Infected' zone dikhayega.")

# File Uploader (Frontend Element)
uploaded_file = st.file_uploader("Upload Drone Image (PNG, JPG, JPEG)...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # 1. Image ko backend mein read karna
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Dimensions nikalna
    rows, cols, _ = image_rgb.shape
    total_pixels = rows * cols

    # 2. Plant Health Index Logic (VARI - Visible Atmospherically Resistant Index)
    # Normal images ke liye: (Green - Red) / (Green + Red)
    green_band = image_rgb[:, :, 1].astype(float)
    red_band = image_rgb[:, :, 0].astype(float)
    
    # Avoid division by zero
    denominator = green_band + red_band
    denominator[denominator == 0] = 1e-5
    
    health_index = (green_band - red_band) / denominator

    # 3. Hotspot Detection (Thresholding)
    # Agar health index slider se set kiye threshold se kam hai, toh woh infected hai
    hotspot_mask = health_index < threshold
    infected_pixels = np.sum(hotspot_mask)
    
    # Calculation for savings
    infected_percentage = (infected_pixels / total_pixels) * 100
    pesticide_saved = 100 - infected_percentage

    # 4. KPI Dashboard Metrics (Frontend Par Results Dikhana)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Field Area Analyzed", value=f"{total_pixels:,} Pixels")
    with col2:
        st.metric(label="🚨 Infected Hotspots Detected", value=f"{infected_percentage:.2f}% Area", delta="- Target Spray Only", delta_color="inverse")
    with col3:
        st.metric(label="💰 Pesticide Chemical Saved", value=f"{pesticide_saved:.2f}% Area", delta="Massive Cost Reduction", delta_color="normal")

    st.markdown("### 📊 Visual Analysis")
    
    # 5. Visualizations generate karke screen par dikhana
    col_img1, col_img2, col_img3 = st.columns(3)
    
    with col_img1:
        st.image(image_rgb, caption="Original Drone Footage", use_container_width=True)
        
    with col_img2:
        # Health Map display (Using Matplotlib colormap)
        fig, ax = plt.subplots()
        im = ax.imshow(health_index, cmap="RdYlGn", vmin=-0.1, vmax=0.4)
        ax.axis('off')
        fig.colorbar(im, ax=ax, orientation='horizontal', pad=0.05)
        st.pyplot(fig)
        st.caption("Crop Health Index Map (Green = Healthy, Red = High Stress)")
        
    with col_img3:
        # Prescription Map Display
        fig2, ax2 = plt.subplots()
        ax2.imshow(hotspot_mask, cmap="binary")
        ax2.axis('off')
        st.pyplot(fig2)
        st.caption("Prescription Map (Black Spots = Target Spray Zones)")

    # 6. Actionable Export Data
    st.markdown("---")
    st.markdown("### 🗺️ GPS / Coordinate Export for Spraying Drones")
    st.write("Yeh coordinates aap direct multi-rotor spraying drone mein load kar sakte hain:")
    
    # Sample coordinates extraction
    hotspot_coords = np.argwhere(hotspot_mask)
    if len(hotspot_coords) > 0:
        st.dataframe(hotspot_coords[:100], column_config={0: "Pixel X Row", 1: "Pixel Y Column"}, use_container_width=True)
        st.info(f"Showing top 100 target coordinates out of {len(hotspot_coords):,} total points.")
    else:
        st.success("Perfect! No infection hotspots detected in this field section.")
else:
    st.info("💡 Awaiting Drone Imagery. Please upload a field photo from the uploader above to trigger the optimizer.")