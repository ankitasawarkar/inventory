# Sagar Furniture - Inventory and Order Management System

## Project Overview

Build Sagar Furniture, an inventory and order-management system for a wooden furniture manufacturer / showroom. The product must support web, tablet, and mobile interfaces, be secure and responsive, and store product images on the host filesystem with metadata in SQLite.

## Target Audience & Users

- **Admin/Manufacturing Manager** — full access: catalogue, orders, manufacturing pipeline, reports, replicate products, add categories/subcategories, inventory adjustments.
- **Showroom Staff / Order Taker** — create customer orders, edit order stages.
- **Customer (public storefront)** — browse catalogue, view development stages, add to cart, request customizations.

## Tech Stack (Recommended)

- **Backend:** Python + FastAPI (ASGI)
- **ORM/DB:** SQLAlchemy (ORM) + SQLite (file DB)
- **Auth:** JWT for API; session/cookie for web UI (if using server-side rendering)
- **Frontend:** React (web), responsive layout for tablet; React Native or PWAs for mobile (shared components)
- **File storage:** Local filesystem (configurable base path); image metadata saved in SQLite with path mapping
- **Testing:** pytest, HTTPX (API tests)
- **Deployment:** Docker (single container for demo), environment variables for paths & secrets
- **Optional:** Alembic for migrations (still supports SQLite), Uvicorn/Gunicorn for production

## High-Level Features

### Catalogue Management

- Categories & subcategories (dynamic)
- Product entries with development stages (raw material → part assembled → polished → photographed → ready to show)
- Multiple images per product and per stage
- Add-to-cart for customers
- Product replication (create new product from existing and allow edits)

### Orders

- On-demand orders (from showroom) & customised items
- Track pipeline per order (design → cut → paint/stain → assemble → polish → pack → ship)
- Link order to product replica

### Inventory & Materials

- Track raw material stock (wood types, finishes, bolts, etc.)
- Decrement inventory on production start / restock endpoints

### Admin Dashboard & Reports

- Current orders and pipeline view
- Production & profit analytics: yearly / monthly / quarterly
- Item validity/warranty, expiry of limited offers

### Image Handling

- Upload images, save to filesystem in structured folders (see logic below)
- Store mapping in SQLite so app can access files reliably

### Security & Auditing

- Role-based access
- Audit trail for critical changes (product edits, order updates, inventory changes)

## Filesystem & Image Mapping Logic (Explicit)

**Configurable MEDIA_ROOT** (env var). Example: `/data/sagar_media/`

On upload, images are stored using this structure:

```
MEDIA_ROOT/
  categories/<category_slug>/
    products/<product_uuid>/  # product-level images
      stage-<stage_name>/     # e.g., raw, assembled, polished
         <image_uuid>_<original_filename>
```

**Image DB table stores:**
- id, product_id, stage, file_path (relative to MEDIA_ROOT), original_name, uploaded_by, created_at

**Image management:**
- When deleting/moving images, update DB and file system; do soft-delete by default (mark deleted_at) and background removal optional.
- Enforce file size limits and allowed MIME types.

## Database Schema (Core Tables) — SQLite

Use SQLAlchemy models or similar

### Key Tables (Fields with Types & Purpose)

#### Category
- `id` (int, PK)
- `name` (str)
- `slug` (str, unique)
- `parent_id` (nullable int, FK to Category) — supports nested subcategories
- `created_at`, `updated_at`

#### Product
- `id` (int, PK)
- `uuid` (str, uuid4)
- `title` (str)
- `sku` (str, unique, optional)
- `category_id` (int, FK)
- `subcategory_id` (int, FK, optional)
- `description` (text)
- `base_price` (decimal)
- `is_customizable` (bool)
- `status` (enum: draft, development, ready, archived)
- `created_by`, `created_at`, `updated_at`

#### ProductDevelopmentStage
Represents development stages for a product
- `id`
- `product_id` (FK)
- `stage_order` (int) — sequence
- `stage_name` (str) — e.g., raw, cut, assembled, polished, finished
- `details` (text) — textual notes, materials used
- `expected_days` (int) — expected days for stage
- `images` — relationship to ProductImage
- `created_at`, `updated_at`

#### ProductImage
- `id`, `product_id`, `stage_id` (nullable), `file_path`, `original_name`, `width`, `height`, `size`, `uploaded_by`, `created_at`, `deleted_at`

#### InventoryItem
- `id`, `name`, `sku`, `unit`, `quantity`, `reorder_level`, `cost_per_unit`, `created_at`, `updated_at`

#### Order
- `id`, `order_number` (str), `customer_name`, `customer_contact`, `status` (enum), `created_at`, `total_amount`, `notes`, `is_custom`, `expected_delivery_date`

#### OrderItem
- `id`, `order_id`, `product_snapshot` (json) — stores product data at time of order (title, options, price), `quantity`, `custom_requirements` (text/json), `unit_price`, `subtotal`

#### Cart
For guest/registered customers
- `id`, `user_id` (nullable), `session_id`, `created_at`, `updated_at`

#### CartItem
- `id`, `cart_id`, `product_id`, `quantity`, `selected_options` (JSON), `added_at`

#### AuditLog
- `id`, `actor_id`, `action_type`, `resource_type`, `resource_id`, `meta` (JSON), `timestamp`

#### ProductionRecord
For manufacturing pipeline snapshots
- `id`, `order_item_id` or `product_id`, `stage_name`, `started_at`, `completed_at`, `operator_id`, `notes`

#### ProfitRecord
- `id`, `product_id`, `order_id`, `revenue`, `costs`, `profit`, `date`

## "Furniture Product Development to Sell" — Table of Required Fields

Fields to capture per product development entry:

- `product_id` (FK)
- `stage_order` (int) — display order
- `stage_name` (string) — e.g., "Raw Material", "Cutting", "Assembly", "Sanding", "Staining", "Polishing", "Photography"
- `stage_description` (text) — description of tasks and acceptance criteria
- `materials_used` (JSON array) — list of inventory items + qty (e.g., `[{item_id, qty, unit}]`)
- `labor_hours_estimate` (decimal)
- `expected_days` (int)
- `actual_days` (int, populated later)
- `quality_checklist` (JSON/text) — list of QC checks and status
- `images` (relation) — multiple images per stage
- `stage_status` (enum) — not_started, in_progress, completed, blocked
- `responsible_person` (FK user id)
- `last_updated` (timestamp)
- `notes` (text)

## APIs — Sample Endpoints & Examples

Note: use REST or GraphQL; below is REST-style suggestions.

### Auth
- `POST /api/auth/login` → returns JWT
- `POST /api/auth/register` (admin only)
- `POST /api/auth/refresh`

### Categories
- `GET /api/categories` — list nested categories
- `POST /api/categories` — create category (admin)
- `PUT /api/categories/{id}` — edit
- `DELETE /api/categories/{id}` — soft delete

### Products & Development
- `GET /api/products` — filters: category, status, search, page
- `GET /api/products/{id}` — full detail incl. stages and images
- `POST /api/products` — create product
- `PUT /api/products/{id}` — update
- `POST /api/products/{id}/replicate` — create a copy (returns new product id) — admin only
- `POST /api/products/{id}/stages` — add development stage
- `PUT /api/products/{id}/stages/{stage_id}` — update stage
- `POST /api/products/{id}/images` — upload images (multipart/form-data)
  - **Behavior:** Save file to structured filesystem path, create ProductImage DB row with relative path.

### Cart & Orders
- `POST /api/cart` — create/update cart (session-based)
- `GET /api/cart/{cart_id}`
- `POST /api/cart/{cart_id}/items` — add item
- `DELETE /api/cart/{cart_id}/items/{item_id}`
- `POST /api/orders` — create order from cart (checkout)
- `GET /api/orders/{id}` — order details and pipeline status
- `POST /api/orders/{id}/items/{item_item_id}/replicate` — admin creates a custom replica order-item from existing product

### Inventory & Production
- `GET /api/inventory` — list materials
- `PATCH /api/inventory/{id}/adjust` — adjust qty (admin)
- `GET /api/production/pipeline` — current pipeline view (grouped by stage)
- `POST /api/production/{record_id}/advance` — move to next stage; update timestamps

### Analytics / Reports
- `GET /api/reports/production?period=monthly&from=2025-01-01&to=2025-03-31`
- `GET /api/reports/profit?period=quarterly`
- `GET /api/reports/item-validity` — items approaching expiry or warranty issues

## UI / UX Required Screens

Design responsive components so they work well on web, tablet, and mobile with a consistent API:

### Public / Customer
- Home / Category listing / Product listing
- Product detail — show development stages in timeline with stage images and descriptions
- Cart and checkout
- Customer order history

### Admin / Internal
- Dashboard: KPIs, pipeline snapshot, quick actions
- Catalogue management: categories, subcategories, product create/edit with drag-drop image uploads
- Product detail with stage editor (add images per stage)
- Order management: list, detail, production timeline, assign operator
- Inventory: material list, adjust, history
- Reports page: filters for year/month/quarter, export CSV/PDF
- Audit logs & user management

### UX Notes
- Show development-stage timeline visually on product page (left: stage name & expected days; right: images & notes).
- Provide inline "replicate" button on product and order-item rows.
- Image gallery should allow reordering and reuse of images across products (to handle repetitive pics).

## Product Replication Flow

1. Admin clicks Replicate on an existing product.
2. System forks a new Product record copying fields and ProductDevelopmentStage rows (deep copy). The new product gets a new uuid and sku.
3. Images are not automatically duplicated on disk; instead:
   - **Option A (default):** reference same image file paths and create new ProductImage rows pointing to same files (cheaper, saves space). Add image_use_count if desired.
   - **Option B (configurable):** copy the image files to the new product folder and create DB entries (physical copy). Provide toggle on replicate endpoint.
4. Admin edits the cloned product fields and stage requirements; then save — it becomes a new distinct product and can be ordered separately.

## Reporting & Analytics Design

- **Profit = revenue — (materials cost + labor cost + overhead)**. Record costs in ProductionRecord and ProfitRecord.
- Provide aggregated SQL queries / ORM methods for:
  - Monthly production count per product
  - Quarterly revenue & profit per product and overall
  - Average lead time per product (avg days from order to shipped)
  - Inventory valuation: `sum(qty * cost_per_unit)`
- Allow CSV and PDF export (server-side generation)

## Validation & Business Rules

- Required fields on product: title, category_id, base_price, at least one image for visibility.
- If `is_customizable` is true, `custom_requirements` allowed in order items.
- Inventory decrements when production stage moves past "materials allocated".
- Order cannot be marked completed unless all pipeline stages have `completed_at`.

## Acceptance Criteria

- ✅ Products, categories and nested subcategories can be created/edited/listed.
- ✅ Admin can upload images; files are saved to filesystem and referenced in SQLite (path correct).
- ✅ Product detail exposes development stages with related images and fields described above.
- ✅ Cart and checkout flow creates orders with item snapshots, supports replicate + small edits for custom orders.
- ✅ Admin can replicate a product into a new product or order item; image reuse logic is handled.
- ✅ Pipeline stage tracking works: start → in progress → completed; timestamps recorded.
- ✅ Reports for yearly / monthly / quarterly production & profit are available and exportable.
- ✅ Role-based authentication and audit logs in place.
- ✅ Automated tests: unit tests for key business rules + integration tests for API endpoints.

## Example SQLAlchemy Model Snippets

```python
# examples only — full models should include relationships and constraints
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    base_price = Column(Numeric(10,2))
    is_customizable = Column(Boolean, default=False)
```

## Suggested Project Structure

```
sagar_furniture/
├─ app/
│  ├─ main.py
│  ├─ api/
│  │  ├─ v1/
│  │  │  ├─ auth.py
│  │  │  ├─ products.py
│  │  │  ├─ orders.py
│  ├─ models/
│  ├─ services/
│  ├─ schemas/  # pydantic schemas
│  ├─ db.py
│  ├─ config.py
├─ migrations/
├─ frontend/   # react app
├─ docker/
├─ tests/
├─ README.md
```

## Testing Checklist (Minimal)

### Unit Tests For:
- product creation, stage lifecycle
- image upload and path mapping
- replicate endpoints (both reference and copy behaviors)
- inventory decrement logic

### Integration Tests:
- cart → checkout → order creation
- pipeline advancement and report generation

### Manual QA:
- responsive UI across mobile/tablet/web
- boundary image sizes and invalid types

## Dev & Deployment Notes

Use `MEDIA_ROOT` and `DATABASE_URL` env variables.

**Example .env:**
```
MEDIA_ROOT=/data/sagar_media
DATABASE_URL=sqlite:///./sagar.db
SECRET_KEY=supersecret
```

**Dockerfile + docker-compose with volumes:**
- Mount a host folder as `/data/sagar_media`
- Mount sqlite db (or use named volume)

For production consider migrating to a server-grade DB (Postgres) when scale demands it.

## Deliverables

1. Working FastAPI backend with documented endpoints (OpenAPI/Swagger).
2. Simple responsive React frontend (web/tablet) that demonstrates flows.
3. Basic mobile PWA or React Native starter to show mobile compatibility.
4. Docker setup for local run + README with run instructions.
5. Tests and sample dataset to seed the app.

## Priority Roadmap (3 Milestones)

1. **MVP (2–3 weeks):** Category and product CRUD, image upload & mapping, product development stage CRUD, cart & order creation, basic replication (reference images), SQLite persistence. Basic admin UI and public product listing.

2. **Manufacturing & Inventory (2 weeks):** Inventory items, production records, pipeline advancement, inventory adjustments, basic reports (CSV).

3. **Analytics & Polish (1–2 weeks):** Profit reporting, quarterly/yearly aggregation, export, audit logs, role management, responsive mobile improvements, tests & docs.

## Example Usage Instructions (Run Locally)

```bash
docker-compose up --build
```

Visit http://localhost:8000/docs for API docs.

Start frontend server (README will include scripts).

## Acceptance Tests & Final Sign-Off

Provide a checklist in PR with screenshots of product page with development timeline and images, sample replicate operation, and exported quarterly report CSV. All endpoints must be covered by integration tests.

## Final Note for the Implementer

- Keep the code modular: separate file storage logic from DB logic with a repository/service layer. Make the image handling pluggable so future migration to cloud object storage (S3) is easy.
- Favor small, well-documented endpoints and clear pydantic models for input validation.
- Ensure reproducible local environment via Docker and seed data for demo.

---

**Next Steps:** This can be converted into:
1. A ready-to-run project scaffold (FastAPI + SQLAlchemy models + sample React pages), or
2. A detailed backlog with JIRA-style tasks & estimated story points.
