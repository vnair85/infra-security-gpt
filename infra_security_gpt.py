import streamlit as st

# --- Backend logic ---
class NetworkInfrastructureAdvisor:
    def get_network_guidance(self, network_type):
        if network_type == "Small Office / Branch Office":
            return (
                "### 🧩 Recommended Setup for Small Office\n"
                "1. **Use a Unified Threat Management (UTM) device**\n"
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

        elif network_type == "Enterprise Campus Network":
            return (
                "### 🏢 Recommended Setup for Enterprise Campus\n"
                "1. **Core-Distribution-Access Layer Topology**\n"
                "   - Ensures scalability and modularity.\n"
                "   - Access layer handles user connectivity, distribution aggregates switches, and core manages high-speed traffic.\n"
                "2. **Redundant Core Switches with OSPF/BGP**\n"
                "   - Offers failover and load balancing capabilities.\n"
                "   - OSPF is preferred for internal routing; BGP for external.\n"
                "3. **NAC (Network Access Control) Integration**\n"
                "   - Verifies user identity and endpoint compliance before granting access.\n"
                "   - Can integrate with AD, RADIUS, or 802.1X.\n"
                "4. **Firewalls between internal zones and internet edge**\n"
                "   - Implements security segmentation (e.g., HR zone, Finance zone).\n"
                "   - Controls East-West and North-South traffic.\n"
                "5. **SD-WAN for Branch Site Integration**\n"
                "   - Offers better performance and flexibility over traditional MPLS.\n"
                "   - Centralized controller can define traffic policies."
            )

        elif network_type == "Cloud-Hybrid Environment":
            return (
                "### ☁️ Hybrid Network Setup\n"
                "1. **Site-to-site VPN or ExpressRoute (Azure)**\n"
                "   - Connects on-premises networks with cloud data centers securely.\n"
                "   - ExpressRoute provides private connection with low latency.\n"
                "2. **Hub-and-Spoke Architecture for Segmentation**\n"
                "   - Central hub VNet manages connectivity and security.\n"
                "   - Spoke VNets for specific workloads (e.g., dev, prod).\n"
                "3. **Use NSGs and Azure Firewall for Traffic Control**\n"
                "   - NSGs manage traffic rules at subnet or NIC level.\n"
                "   - Azure Firewall inspects and logs network traffic.\n"
                "4. **Enforce Routing Tables and DNS Forwarding**\n"
                "   - Custom route tables help control traffic flow between subnets.\n"
                "   - Forward DNS requests to on-prem DNS if hybrid.\n"
                "5. **Integrate with On-Prem AD/LDAP Securely**\n"
                "   - Use Azure AD Connect with password hash sync or pass-through auth.\n"
                "   - Deploy AD DS in Azure if full hybrid is needed."
            )

        else:
            return "❗ Please select a valid network type."

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
    st.markdown(advisor.get_network_guidance(network_type))
