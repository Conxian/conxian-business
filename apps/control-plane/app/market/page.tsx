import { PublicServicePage } from "../../components/public-service-page";

export const metadata = { title: "Market | Conxian Labs", description: "Conxian Market client and asset surface." };

export default function MarketPage() {
  return <PublicServicePage eyebrow="Conxian Market" title="A clear place for governed assets and services." description="Discover Conxian offerings, understand their trust boundaries, and start the right client or partner conversation." audience="Clients, partners, and service teams" capabilities={["Service discovery", "Asset and catalog surfaces", "Governed partner onboarding"]} runtime="Market operations and moderation remain protected by the BOS control plane." />;
}
