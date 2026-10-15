-- AlterTable
ALTER TABLE "NeighborSignal" ADD COLUMN "authorId" UUID;

-- Backfill: учебные сигналы привязываем к демонстрационному соседу.
UPDATE "NeighborSignal"
SET "authorId" = (SELECT "id" FROM "User" WHERE "email" = 'neighbor@example.test' LIMIT 1)
WHERE "authorId" IS NULL;

-- Если демо-пользователя ещё нет, создаём временную привязку нельзя — требуем NOT NULL после fill.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM "NeighborSignal" WHERE "authorId" IS NULL) THEN
    RAISE EXCEPTION 'NeighborSignal.authorId backfill failed: no demo user';
  END IF;
END $$;

ALTER TABLE "NeighborSignal" ALTER COLUMN "authorId" SET NOT NULL;

-- CreateIndex
CREATE INDEX "NeighborSignal_authorId_idx" ON "NeighborSignal"("authorId");

-- AddForeignKey
ALTER TABLE "NeighborSignal" ADD CONSTRAINT "NeighborSignal_authorId_fkey" FOREIGN KEY ("authorId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
