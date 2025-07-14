import streamlit as st

# --- Backend logic ---
class NetworkInfrastructureAdvisor:
    def get_network_guidance(self, network_type):
        if network_type == "Small Office / Branch Office":
            return (
                "### 🧩 Recommended Setup for Small Office\n"
                "- Use a Unified Threat Management (UTM) device for firewall + IDS/IPS\n"
                "- VPN-enabled router with VLAN segmentation\n"
                "- Secure Wi-Fi with WPA3 and MAC filtering\n"
                "- Setup site-to-site VPN for HQ access\n"
                "- Cloud-managed switch (Layer 2 or 3)"
            )
        elif network_type == "Enterprise Campus Network":
            return (
                "### 🏢 Recommended Setup for Enterprise Campus\n"
                "- Core-Distribution-Access layer topology\n"
                "- Redundant core switches with OSPF/BGP\n"
                "- NAC (Network Access Control) integration\n"
                "- Firewalls between internal zones and internet edge\n"
                "- SD-WAN for branch site integration"
            )
        elif network_type == "Cloud-Hybrid Environment":
            return (
                "### ☁️ Hybrid Network Setup\n"
                "- Site-to-site VPN or ExpressRoute (Azure)\n"
                "- Hub-and-spoke architecture for segmentation\n"
                "- Use NSGs and Azure Firewall for traffic control\n"
                "- Enforce routing tables and DNS forwarding\n"
                "- Integrate with on-prem AD/LDAP securely"
            )
        else:
            return "❗ Please select a valid network type."

# --- Streamlit UI ---
st.set_page_config(page_title="Network Infra Advisor", page_icon="🧩")
st.title("🧩 Network Infrastructure Advisor")

advisor = NetworkInfrastructureAdvisor()

st.markdown("""
This module provides network architecture best practices for various organizational setups.
Select your environment below to get expert design recommendations.
""")

network_type = st.selectbox("Select your network environment:", [
    "Small Office / Branch Office",
    "Enterprise Campus Network",
    "Cloud-Hybrid Environment"
])

if st.button("Get Recommendations"):
    st.markdown(advisor.get_network_guidance(network_type))
