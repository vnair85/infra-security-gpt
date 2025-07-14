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
                "2. **[VPN-enabled router with VLAN segmentation](#vpn-vlan-guide)**\n"
                "   - Enables secure remote access for employees.\n"
                "   - VLANs help separate traffic (e.g., guest vs internal).\n"
                "3. **[Secure Wi-Fi with WPA3 and MAC filtering](#wifi-guide)**\n"
                "   - WPA3 offers the latest encryption standards for wireless security.\n"
                "   - MAC filtering ensures only known devices connect.\n"
                "4. **[Setup site-to-site VPN for HQ access](#site-vpn-guide)**\n"
                "   - Allows secure traffic between branch and headquarters.\n"
                "   - Typically uses IPsec tunnels with static IP configuration.\n"
                "5. **[Cloud-managed switch (Layer 2 or 3)](#switch-guide)**\n"
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

    def get_vpn_vlan_guide(self):
        return (
            "### 🔐 How to Set Up VPN-Enabled Router with VLANs\n"
            "1. **Choose a router with VPN and VLAN support**\n"
            "   - Look for devices like Cisco RV340, Ubiquiti EdgeRouter, MikroTik.\n"
            "2. **Access the router’s admin page**\n"
            "   - Usually accessible via IP like 192.168.1.1\n"
            "3. **Configure VPN (IPSec, SSL, or L2TP)**\n"
            "   - Create VPN user profiles and pre-shared keys.\n"
            "   - Enable remote access and test with VPN client.\n"
            "4. **Create VLANs for network segmentation**\n"
            "   - Assign different VLAN IDs to different types of users (e.g., VLAN10: Internal, VLAN20: Guests).\n"
            "5. **Configure port or SSID VLAN tagging**\n"
            "   - Ensure switches and access points tag traffic correctly.\n"
            "6. **Enable inter-VLAN routing if needed**\n"
            "   - Allow controlled access between VLANs using ACLs or firewall rules."
        )

    def get_wifi_guide(self):
        return (
            "### 📶 How to Secure Wi-Fi with WPA3 and MAC Filtering\n"
            "1. **Use a modern wireless access point or router**\n"
            "   - Ensure it supports WPA3 (e.g., Ubiquiti UniFi, Aruba InstantOn).\n"
            "2. **Enable WPA3 Encryption**\n"
            "   - Set Wi-Fi security settings to WPA3-Personal or WPA3-Enterprise.\n"
            "3. **Configure strong passphrase**\n"
            "   - Use a minimum of 12–16 characters, avoid dictionary words.\n"
            "4. **Enable MAC filtering**\n"
            "   - Whitelist devices by their MAC addresses in router settings.\n"
            "5. **Disable WPS and remote admin access**\n"
            "   - Prevent physical button-based access and limit management exposure."
        )

    def get_site_vpn_guide(self):
        return (
            "### 🌐 How to Set Up Site-to-Site VPN\n"
            "1. **Ensure both sites have static public IPs**\n"
            "   - Required to establish stable IPsec tunnels.\n"
            "2. **Login to UTM/router GUI of both ends**\n"
            "   - Navigate to VPN/IPsec section.\n"
            "3. **Create IPsec Phase 1 & Phase 2 tunnels**\n"
            "   - Define encryption settings (AES-256, SHA256, DH Group 14).\n"
            "4. **Set local and remote subnets**\n"
            "   - Example: 192.168.1.0/24 <-> 192.168.2.0/24\n"
            "5. **Apply firewall rules to allow VPN traffic**\n"
            "   - Allow ESP, IKE, and NAT-T protocols.\n"
            "6. **Monitor tunnel status and logs**\n"
            "   - Ensure tunnel is active and stable."
        )

    def get_switch_guide(self):
        return (
            "### 🔌 How to Deploy a Cloud-Managed Switch\n"
            "1. **Choose a cloud-managed switch (e.g., Cisco Meraki, Aruba)**\n"
            "   - Register it in the cloud dashboard using serial number.\n"
            "2. **Connect to internet and power**\n"
            "   - Use uplink port to connect to internet router or firewall.\n"
            "3. **Login to cloud dashboard**\n"
            "   - Access configuration panel online (Meraki Dashboard, Aruba Central).\n"
            "4. **Configure VLANs and port profiles**\n"
            "   - Assign tagged VLANs to switch ports.\n"
            "5. **Enable monitoring and alerts**\n"
            "   - Set thresholds for bandwidth, errors, link status.\n"
            "6. **Apply firmware updates**\n"
            "   - Keep the switch secure and feature-rich."
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

# Expandable guides for each point
st.markdown("---")
with st.expander("📘 Click here to learn how to set up a UTM device (Point 1)"):
    st.markdown(advisor.get_utm_guide())

with st.expander("📘 Click here to configure VPN + VLAN (Point 2)"):
    st.markdown(advisor.get_vpn_vlan_guide())

with st.expander("📘 Click here to secure Wi-Fi with WPA3 + MAC filter (Point 3)"):
    st.markdown(advisor.get_wifi_guide())

with st.expander("📘 Click here to set up site-to-site VPN (Point 4)"):
    st.markdown(advisor.get_site_vpn_guide())

with st.expander("📘 Click here to deploy a cloud-managed switch (Point 5)"):
    st.markdown(advisor.get_switch_guide())
