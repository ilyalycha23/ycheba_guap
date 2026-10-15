-- AlterTable
ALTER TABLE "NeighborSignal" ADD COLUMN "archivedAt" TIMESTAMPTZ(3);

-- CreateIndex
CREATE INDEX "NeighborSignal_archivedAt_idx" ON "NeighborSignal"("archivedAt");
