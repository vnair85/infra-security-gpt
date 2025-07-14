import streamlit as st

# --- Backend logic ---
class NetworkInfrastructureAdvisor:
    def get_network_guidance(self, network_type):
        if network_type == "Small Office / Branch Office":
            return (
                "### 🧩 Recommended Setup for Small Office\n"
                "1. **[Use a Unified Threat Management (UTM) device](#utm-guide)**\n"
                "   - Combines firewall, antivirus, content filtering, and IDS/IPS into one appliance.\n"
                "   - Ideal for small teams without a dedicated security team.\n"
                "2. **VPN-enabled router with VLAN segmentation**\n"
                "   - Enables secure remote access for employees.\n"
                "   - VLANs help separate traffic (e.g., guest vs internal).\n"
                "3. **Secure Wi-Fi with WPA3 and MAC filtering**\n"
                "   - WPA3 offers the latest encryption standards for wireless security.\n"
                "   - MAC filtering ensures only known devices connect.\n"
                "4. **Setup site-to-site VPN for HQ access**\n"
                "   - Allows secure traffic between branch and headquarters.\n"
                "   - Typically uses IPsec tunnels with static IP configuration.\n"
                "5. **Cloud-managed switch (Layer 2 or 3)**\n"
                "   - Provides centralized visibility and control via a web console.\n"
                "   - Layer 3 switching can also handle routing if needed."
            )
        else:
            return "❗ Please select a valid network type."

    def get_utm_guide(self):
        return (
            "### 🛠️ How to Set Up a UTM Device\n"
            "1. **Choose a UTM Appliance**\n"
            "   - Common options: FortiGate, Sophos XG, pfSense (open source).\n"
            "2. **Connect Hardware**\n"
            "   - WAN port to ISP modem/router.\n"
            "   - LAN port to switch or internal network.\n"
            "3. **Access Web GUI**\n"
            "   - Default IP usually 192.168.1.1\n"
            "   - Login with default credentials, then change password.\n"
            "4. **Run Initial Wizard**\n"
            "   - Set timezone, hostname, internal IP range.\n"
            "   - Enable DHCP if needed.\n"
            "5. **Configure Firewall Rules**\n"
            "   - Allow internal → internet, block external → internal.\n"
            "6. **Enable Additional Services**\n"
            "   - Enable IPS, antivirus, web filtering based on licensing.\n"
            "7. **Save & Monitor Logs**\n"
            "   - Enable email alerts and syslog integration."
        )

# --- Streamlit UI ---
st.set_page_config(page_title="Network Infra Advisor", page_icon="🧩")
st.title("🧩 Network Infrastructure Advisor")

advisor = NetworkInfrastructureAdvisor()

st.markdown("""
This module provides network architecture best practices for various organizational setups.\n
Each point below includes detailed guidance to help you design secure, scalable, and efficient networks.
""")

network_type = st.selectbox("Select your network environment:", [
    "Small Office / Branch Office",
    "Enterprise Campus Network",
    "Cloud-Hybrid Environment"
])

if st.button("Get Recommendations"):
    st.markdown(advisor.get_network_guidance(network_type), unsafe_allow_html=True)

# Expandable guide for Point 1 (UTM Device)
st.markdown("---")
with st.expander("📘 Click here to learn how to set up a UTM device (Point 1)"):
    st.markdown(advisor.get_utm_guide())
