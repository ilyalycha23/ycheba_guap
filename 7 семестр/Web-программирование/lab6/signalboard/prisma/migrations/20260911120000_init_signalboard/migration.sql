-- CreateTable
CREATE TABLE "User" (
    "id" UUID NOT NULL,
    "name" VARCHAR(80) NOT NULL,
    "email" VARCHAR(254) NOT NULL,
    "passwordHash" VARCHAR(255) NOT NULL,
    "createdAt" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ(3) NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "NeighborSignal" (
    "id" UUID NOT NULL,
    "slug" VARCHAR(80) NOT NULL,
    "title" VARCHAR(160) NOT NULL,
    "summary" TEXT NOT NULL,
    "category" VARCHAR(40) NOT NULL,
    "location" VARCHAR(240) NOT NULL,
    "image" VARCHAR(240) NOT NULL,
    "imageAlt" VARCHAR(240) NOT NULL,
    "latitude" DECIMAL(9,6) NOT NULL,
    "longitude" DECIMAL(9,6) NOT NULL,
    "createdAt" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ(3) NOT NULL,

    CONSTRAINT "NeighborSignal_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "TrackedSignal" (
    "userId" UUID NOT NULL,
    "signalId" UUID NOT NULL,
    "createdAt" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "TrackedSignal_pkey" PRIMARY KEY ("userId","signalId")
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "NeighborSignal_slug_key" ON "NeighborSignal"("slug");

-- CreateIndex
CREATE INDEX "TrackedSignal_signalId_idx" ON "TrackedSignal"("signalId");

-- AddForeignKey
ALTER TABLE "TrackedSignal" ADD CONSTRAINT "TrackedSignal_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TrackedSignal" ADD CONSTRAINT "TrackedSignal_signalId_fkey" FOREIGN KEY ("signalId") REFERENCES "NeighborSignal"("id") ON DELETE CASCADE ON UPDATE CASCADE;
