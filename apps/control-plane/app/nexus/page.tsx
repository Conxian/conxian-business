import { PublicServicePage } from "../../components/public-service-page";

export const metadata = { title: "Nexus | Conxian Labs", description: "Conxian Nexus orchestration and policy surface." };

export default function NexusPage() {
  return <PublicServicePage eyebrow="Conxian Nexus" title="Orchestration with policy at the center." description="Coordinate trusted workflows, policy decisions, and service interactions across the Conxian ecosystem." audience="Teams building governed automation" capabilities={["Workflow orchestration", "Policy-aware execution", "Cross-service coordination"]} runtime="Nexus runtime health and readiness are verified independently from this public surface." />;
}
