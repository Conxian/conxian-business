import { DataTable, StatusBadge } from "../../components/data-table";
import { getCurrentActor } from "../../lib/auth";
import { PageHeader } from "../../components/page-header";
import { getEnvironmentData } from "../../lib/module-adapters";
import { requireControlPlaneAccess } from "../../lib/auth";
import type { EnvironmentRecord } from "@conxian/schemas";

export default async function EnvironmentsPage() {
  const actor = await getCurrentActor(await headers());
  const environments = await getEnvironmentData();

  return (
    <main className="page-shell">
      <PageHeader
        eyebrow="Module"
        title="Environments"
        description="Track environment ownership, classification, and verification state."
        actor={actor}
      />

      <section className="card">
        <h3>Registry</h3>
        <DataTable<EnvironmentRecord>
          columns={[
            { key: "name", header: "Environment", render: (item) => item.name },
            { key: "classification", header: "Classification", render: (item) => item.classification },
            { key: "owner", header: "Owner", render: (item) => item.owner },
            {
              key: "verificationStatus",
              header: "Verification",
              render: (item) => <StatusBadge value={item.verificationStatus} />,
            },
          ]}
          rows={environments}
        />
      </section>
    </main>
  );
}
