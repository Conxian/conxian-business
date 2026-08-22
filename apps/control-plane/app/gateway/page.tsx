import { PublicServicePage } from "../../components/public-service-page";

export const metadata = { title: "Gateway | Conxian Labs", description: "Conxian Gateway integration and protocol surface." };

export default function GatewayPage() {
  return <PublicServicePage eyebrow="Conxian Gateway" title="A dependable boundary for every integration." description="Connect client systems to Conxian capabilities through explicit protocols, authenticated requests, and observable service boundaries." audience="Client and M2M integrators" capabilities={["Protocol gateway", "M2M authentication", "Health and readiness contracts"]} runtime="Gateway runtime health and readiness are verified independently from this public surface." />;
}
