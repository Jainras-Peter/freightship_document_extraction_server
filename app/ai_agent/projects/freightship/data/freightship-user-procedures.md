# FreightShip — User procedures (RAG knowledge base)

Use this file as **source chunks** for a vector DB. Each section is self-contained: keep a section + its steps together when chunking, or split on `---` boundaries.

**Product:** FreightDocs — freight document generation and booking management.  
**Key routes:** `/generate`, `/generate/result`, `/dashboard`, `/booking/shipper`, `/booking/shipment`, `/booking/status`, `/profile` (forwarder profile).

---

## Q: How do I generate an HBL from an MBL? / MBL to HBL conversion / Document to Document flow

**Synonyms:** create HBL from master bill; convert MBL scan to house bill; Doc to Doc; Document to Document.

**Prerequisites:** You are logged in. You have an MBL file (PDF, PNG, or JPG, max 10 MB).

**Steps:**

1. Open the **Generate** page (`/generate`).
2. In the left sidebar under **Generation Mode**, select **Document to Document** (subtitle: *MBL to HBL Conversion*). If the sidebar is collapsed, use the document icon, then choose Document to Document.
3. **Step 1 — Upload (Setup & Upload):**
   - Under **From**, choose the input document type (Master Bill of Lading / MBL as appropriate).
   - Under **To**, choose the output type (House Bill of Lading / HBL as appropriate).
   - Under **Model**, pick the AI model.
   - Click the upload area (or **Drop MBL scan here**) and select your MBL file.
   - Click **Start Process** and wait while the document is processed.
4. **Step 2 — Details (Document Details):**
   - Confirm or enter the **Master BL Number** (e.g. `MBL-LA-2024-9981`).
   - Under **Select Shipment(s)**, choose the shipment(s) linked to this MBL. If you see *No shipper linked with this MBL*, create shippers and shipments in **Booking Manager** first, and sync the MBL to those shipments (see “Sync MBL number with shipment”).
   - Click **Generate Preview**.
5. **Step 3 — Finalize (Review & Finalize):**
   - Review validation and accuracy scores.
   - Use **Edit Document** if you need to correct fields, then **Save Changes**.
   - Click **Confirm & Generate** to submit and generate the HBL(s).
6. **Step 4 — Download:** After success, use the result screen or dashboard to download files (see “How do I download and view generated documents?”).

**Related:** **Info to Document** (`/generate`, left sidebar) is for **manual data entry** into templates (including Bill of Lading) without uploading an MBL first.

---

## Q: How do I sync an MBL number with a shipment? / Link MBL to booking / Attach master BL to shipment

**Synonyms:** associate MBL with shipment; MBL booking; master bill sync.

**Where:** **Booking Manager** → **Shipment** (`/booking/shipment`).

**Method A — Create Booking (recommended for linking MBL to one or more shipments):**

1. Go to **Booking** → **Shipment** in the sidebar (`/booking/shipment`).
2. Click **Create Booking**.
3. Enter the **MBL Number** (required).
4. Select **Mode**: **FCL** or **LCL** (required).
5. **Select Shipment(s):**
   - **FCL:** choose exactly **one** unsynced FCL shipment from the dropdown.
   - **LCL:** tick up to **five** unsynced LCL shipments (only shipments not already showing MBL synced status are listed).
6. Optionally fill **Carrier Name**, **Est. Departure Date**, and **Est. Arrival Date**.
7. Click **Confirm Booking**. On success, shipments update and the table **MBL** column shows the number; **Status** can show **MBL number Sycned** when applicable.

**Method B — Shipment Details & MBL Sync dialog (per-shipment sync):**

1. On **Shipment** (`/booking/shipment`), open the **Shipment Details & MBL Sync** dialog for the target shipment (when available from the product UI).
2. Enter **Master Bill of Lading (MBL) Number** (required), optional **Carrier Name**, **Est. Departure Date**, **Est. Arrival Date**.
3. Click **Confirm & Sync**. If the MBL is already synced for that row, fields appear read-only and the dialog shows **Synced**.

**Note:** Shipments must have **Mode** (FCL/LCL) set before sync can succeed.

---

## Q: How do I create a shipper?

**Synonyms:** add shipper; register shipper; new shipper record.

**Steps:**

1. Go to **Booking** → **Shipper** (`/booking/shipper`).
2. Click **Add Shipper**.
3. In the dialog, complete **Shipper ID**, **Contact**, **Shipper Name**, and **Address** (required fields).
4. Click **Add Shipper** to save.

**Edit / delete:** Use the pencil (**Edit**) or trash (**Delete**) actions in the shippers table.

---

## Q: How do I create a forwarder? / Forwarder company setup

**Synonyms:** freight forwarder account; company profile; forwarder details.

**Important:** There is **no separate “Forwarder” screen under Booking**. The forwarder is tied to the **user account**.

**Steps:**

1. **At signup:** On **Sign up**, enter **Forwarder Company Name** (required) along with your account details.
2. **After login:** Open **Profile** (`/profile`) — **Forwarder Profile** — to view or update forwarder/company details.

---

## Q: How do I create a shipment?

**Synonyms:** add shipment; new booking line; shipment specifications.

**Prerequisites:** At least one **Shipper** exists (`/booking/shipper`).

**Steps:**

1. Go to **Booking** → **Shipment** (`/booking/shipment`).
2. Click **Add Shipment**.
3. **Shipper** (required): select from the dropdown (shipper name and ID).
4. **Mode** (required): **LCL** or **FCL**.
5. Fill optional fields as needed: **Cargo Type**, **Goods Description**, weights, **Origin**, **Destination**, **Desired Delivery Date**, **Packages Count**, **Special Requirements**, **Marks and Numbers**, **Measurement**, etc.
6. Click **Add Shipment** (or **Update Shipment** when editing).

**Shipment ID:** Shown as auto-generated on save when adding new.

**After creating shipments:** Use **Create Booking** or the MBL sync flow to attach an **MBL number** so they appear for **Document to Document** generation.

---

## Q: How do I download and view generated documents? / Where are my PDFs?

**Synonyms:** get HBL PDF; open last generated file; document history.

**Option 1 — Immediately after generation (`/generate/result`):**

1. After a successful run, you are taken to the **document generation result** page.
2. Each file appears in a list with a **download** link (opens in a new tab).
3. Use **Download All** to fetch an archive when multiple files exist.
4. Use **Go to Dashboard** to jump to the full document list.

**Option 2 — Dashboard (`/dashboard`):**

1. Open **Dashboard** from navigation.
2. In **Recently Generated Documents**, find the row by **DOCUMENT NAME**, **TYPE**, or **DATE**.
3. **Download:** click the download action (same behavior as opening the file URL).
4. **View:** use the view action (opens the document URL).
5. **Filter by Type** using the dropdown above the table if you have many documents.
6. **Delete:** use the delete action if you need to remove a stored document.

**Tip:** From the dashboard header you can also start **New Document**, which routes to `/generate`.

---

## Q: What is the difference between Document to Document and Info to Document?

| Mode | Sidebar label | Purpose |
|------|----------------|---------|
| Document to Document | *MBL to HBL Conversion* | Upload a source document (e.g. MBL scan), extract data, map to shipments, preview, generate HBL-style output. |
| Info to Document | *Manual Data Entry* | Fill template fields (e.g. Bill of Lading, Commercial Invoice, Quotation) by hand, then save/download from that flow. |

---

## Q: What are the steps in the Document to Document wizard?

1. **Upload** — document types, model, file upload, **Start Process**.  
2. **Details** — Master BL number, **Select Shipment(s)**, **Generate Preview**.  
3. **Finalize** — scores, edit, **Confirm & Generate**.  
4. **Download** — retrieve files from result page and/or dashboard.

---

## Q: Where do I see booking status?

Go to **Booking** → **Status** (`/booking/status`) from the Booking Manager sidebar.

---

## Chunking hints (for implementers)

- Duplicate short **“Prerequisites”** lines in chunks that need them for retrieval.  
- Index both **questions** and **synonym** lines.  
- Keep **Method A / Method B** subsections in the same chunk as the MBL sync main question when possible.  
- UI spelling **“MBL number Sycned”** matches the application status string; include the typo in embeddings if users quote the UI.
