# Q2O Validation Reference — Confluence Page Content

## Purpose
This document explains what each of the 55 validations **currently running on the UI** actually checks. These validations are all performed automatically by the validation agent — the end user never performs the check themselves, they only see the pass/fail result on screen. This reference exists so that, when a user sees a validation on screen and isn't sure what it means, they can look it up here.

## How to use this doc
- Each validation below is formatted as its own Confluence page: a two-column table (Field → Details), exactly matching your spec.
- **Additional Comments** (process guidance, e.g. "raise via MDG") sit *below* the table, not inside it — per your original instruction.
- **Examples / screenshots** are left as a placeholder under each entry for you to add manually.
- Copy each `###` section into its own new Confluence page.

### Two assumptions to confirm
1. **Validation Type** — I used a binary split: **Base** (runs on every order) vs **Conditional** (only applies in a specific scenario, stated in the Rule Description). This follows the pattern from your Customer Name example (Type: Base). If your team uses different category names, tell me and I'll relabel all 55 in one pass.
2. **Status** — defaulted to **Developed** across the board, since the source doc states these are all currently live on the UI. If any are actually mid-refinement or need clarification, flag which IDs and I'll update just those.

---

## Index

| ID | Validation Name | Type |
|---|---|---|
| R1 | PO or Signed Contract Provided | Base |
| R2 | Customer Quote Provided | Base |
| R3 | Vendor Quote & Vendor Instruction | Base |
| R4 | Site ID Provided | Base |
| R5 | Site Contact Information Provided | Base |
| R6 | Sales Summary / Design (HLD) Provided | Conditional |
| R7 | Summary Completeness (Services, Deployment, Engineering, Leadtime) | Base |
| C1 | Leadtime Aligned to Product KPIs | Conditional |
| C2 | Circuit Order Form Attached | Conditional |
| C3 | Signed PO/Quote Attached | Base |
| C4 | Vendor Identified | Base |
| C5 | Third-Party Vendor Quotes Attached | Conditional |
| C6 | Infra Orders Correct (Sales Enablement) | Base |
| C7 | Site Information Correct | Base |
| C8 | Site Contact Details Complete | Base |
| C9 | Summary/Design Matches Order Form | Base |
| C10 | Correct Billing Account/Company Name | Base |
| C11 | Customer LAN IP Details Provided (DIA) | Conditional |
| C12 | Public IP Address Range Approved | Conditional |
| C13 | IP Address Range Within Standard Offering | Conditional |
| C14 | Kit, Router Compatibility & Fulfilment Correct | Base |
| C15 | Accessories & Licences Complete | Base |
| C16 | Third-Party Installation Included in Quote | Conditional |
| C17 | Contract Term Matches Order | Base |
| C18 | B-End Information Correct | Conditional |
| C19 | QoS (AF/EF %) Correct | Conditional |
| C20 | Cease Details Included (If Applicable) | Conditional |
| C21 | Upgrade/Downgrade Clearly Stated | Conditional |
| C22 | Referenced Email/File Attached | Conditional |
| C23 | Vendor Quote Still Valid | Base |
| C24 | Vodafone Quote to Customer Attached | Base |
| C25 | Customer-Communicated Leadtime Captured | Base |
| C26 | Vendor Quotations Attached | Base |
| C27 | Commercial Approval Included in Tech Spec | Base |
| B1 | Customer Name Exists & Matches in BSP | Base |
| B2 | Delivery Address Exists in BSP | Base |
| B3 | Billing Entity Matches BSP Bill-To Name | Base |
| B4 | Opportunity Reference Matches VBOP | Base |
| B5 | PO Number Consistent Across Sources | Base |
| B6 | Vendor Cost Price Below Sell Price | Base |
| B7 | Tech Spec Product Codes Present in Vendor Quote | Base |
| B8 | Tech Spec Product Codes Exist in BSP (MDM) | Base |
| B9 | Quantities Align Across Documents | Base |
| B10 | Vendor Quote Within 30-Day Validity | Base |
| B11 | Tech Spec Contact Details Complete | Base |
| B13 | Billing Address Present & Exists in BSP | Base |
| X1 | Contract Term Present (Circuit) | Conditional |
| X2 | Premise ID Present (SIRO) | Conditional |
| X3 | Service Type Matches Supporting Docs | Conditional |
| X4 | Speed Matches Customer Order Form | Conditional |
| X5 | Product Name & Type Present | Conditional |
| X6 | Service Address Matches BSP | Conditional |
| X7 | Circuit Order Form PO Matches VBOP | Conditional |
| X8 | Billing Frequency Present & Aligned | Conditional |
| X9 | PO Type Set to Recurring | Conditional |

*Note: B12 does not appear in the source UI list — the BSP checks run from B1–B11 then B13. Preserved as-is; flag if this was meant to exist.*

---

## Required Information

### R1 — PO or Signed Contract Provided

| Field | Details |
|---|---|
| Validation Name | PO or Signed Contract Provided |
| Rule Description | Confirms that a valid purchase order or signed contract has been provided to authorize the order. |
| Pass Criteria | 1. A PO or signed contract document is attached to the request. |
| Validation Type | Base |
| Failed Action | No PO or signed contract is attached; the request cannot proceed until one is provided. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R2 — Customer Quote Provided

| Field | Details |
|---|---|
| Validation Name | Customer Quote Provided |
| Rule Description | Confirms the quote issued to the customer for this order is included with the request. |
| Pass Criteria | 1. The quote provided to the customer is attached. |
| Validation Type | Base |
| Failed Action | Customer quote is missing; requestor must attach it. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R3 — Vendor Quote & Vendor Instruction

| Field | Details |
|---|---|
| Validation Name | Vendor Quote & Vendor Instruction |
| Rule Description | Confirms a vendor quote is attached and that the documentation clearly states which vendor the order should be placed with. |
| Pass Criteria | 1. Vendor quote is attached.<br>2. The vendor to order from is clearly and unambiguously stated. |
| Validation Type | Base |
| Failed Action | Vendor quote missing and/or vendor not clearly identified; requestor must clarify. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R4 — Site ID Provided

| Field | Details |
|---|---|
| Validation Name | Site ID Provided |
| Rule Description | Confirms the Site ID for the order location has been provided. |
| Pass Criteria | 1. Site ID is present in the documentation. |
| Validation Type | Base |
| Failed Action | Site ID missing; requestor must provide it. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R5 — Site Contact Information Provided

| Field | Details |
|---|---|
| Validation Name | Site Contact Information Provided |
| Rule Description | Confirms contact details for the site are included with the request. |
| Pass Criteria | 1. Site contact name provided.<br>2. Contact details (email and/or phone) provided. |
| Validation Type | Base |
| Failed Action | Site contact info is missing or incomplete. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R6 — Sales Summary / Design (HLD) Provided

| Field | Details |
|---|---|
| Validation Name | Sales Summary / Design (HLD) Provided |
| Rule Description | Confirms a summary of what was sold is provided, and — where Solution Design is involved — that a High-Level Design (HLD) is included. |
| Pass Criteria | 1. Summary of sold services present.<br>2. If Solution Design is involved, HLD/design document is attached. |
| Validation Type | Conditional — HLD requirement only applies when Solution Design is involved |
| Failed Action | Summary missing, or HLD missing when Solution Design is involved. |
| Status | Developed |

*Examples/screenshots: to be added.*

### R7 — Summary Completeness (Services, Deployment, Engineering, Leadtime)

| Field | Details |
|---|---|
| Validation Name | Summary Completeness (Services, Deployment, Engineering, Leadtime) |
| Rule Description | Confirms the order summary covers all required elements: services supplied, deployment details, engineering asks/requirements, and leadtime. |
| Pass Criteria | 1. Services supplied described.<br>2. Deployment details described.<br>3. Engineering asks/requirements described.<br>4. Leadtime stated. |
| Validation Type | Base |
| Failed Action | One or more required summary elements missing; requestor must complete the summary. |
| Status | Developed |

*Examples/screenshots: to be added.*

---

## Document Checks

### C1 — Leadtime Aligned to Product KPIs

| Field | Details |
|---|---|
| Validation Name | Leadtime Aligned to Product KPIs |
| Rule Description | Where a leadtime has been communicated to the customer, validates that it aligns with the company's published Product KPIs for that service. |
| Pass Criteria | 1. If a leadtime was provided to the customer, it matches or is consistent with the applicable Product KPI. |
| Validation Type | Conditional — only applies if a leadtime was provided to the customer |
| Failed Action | Leadtime communicated does not align with Product KPIs; flag for review with sales/commercial. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C2 — Circuit Order Form Attached

| Field | Details |
|---|---|
| Validation Name | Circuit Order Form Attached |
| Rule Description | Confirms the Circuit Order Form is attached for circuit-related orders. |
| Pass Criteria | 1. Circuit Order Form is attached. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Circuit Order Form missing; requestor must attach it. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C3 — Signed PO/Quote Attached

| Field | Details |
|---|---|
| Validation Name | Signed PO/Quote Attached |
| Rule Description | Confirms the customer PO or quote is attached and carries a signature. |
| Pass Criteria | 1. PO or quote document attached.<br>2. Document is signed. |
| Validation Type | Base |
| Failed Action | PO/Quote missing or unsigned. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C4 — Vendor Identified

| Field | Details |
|---|---|
| Validation Name | Vendor Identified |
| Rule Description | Confirms the documentation clearly states which vendor the order is being placed with. |
| Pass Criteria | 1. Vendor is unambiguously named in the documentation. |
| Validation Type | Base |
| Failed Action | Vendor not clearly stated; request sent back for clarification. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C5 — Third-Party Vendor Quotes Attached

| Field | Details |
|---|---|
| Validation Name | Third-Party Vendor Quotes Attached |
| Rule Description | Where a third-party network provider is used (Eir Fibre, Eir UG, EIL and SAB, Enet, Siro, Ripplecom/Host), confirms the relevant third-party quote is attached. |
| Pass Criteria | 1. If a third party from the approved list is used, their quote is attached. |
| Validation Type | Conditional — only applies when a listed third party is involved |
| Failed Action | Third party used but quote not attached. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C6 — Infra Orders Correct (Sales Enablement)

| Field | Details |
|---|---|
| Validation Name | Infra Orders Correct (Sales Enablement) |
| Rule Description | Confirms the correct Sales Enablement infrastructure orders are attached and that product type, speed, and related attributes match the order. |
| Pass Criteria | 1. Infra order(s) attached.<br>2. Product on infra order matches order.<br>3. Speed and other attributes match order. |
| Validation Type | Base |
| Failed Action | Infra order missing or mismatched on product, speed, or other attributes. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C7 — Site Information Correct

| Field | Details |
|---|---|
| Validation Name | Site Information Correct |
| Rule Description | Confirms Site ID, Site Name, and Site Address are all present and correct. |
| Pass Criteria | 1. Site ID correct.<br>2. Site Name correct.<br>3. Site Address correct. |
| Validation Type | Base |
| Failed Action | One or more site details missing or incorrect. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C8 — Site Contact Details Complete

| Field | Details |
|---|---|
| Validation Name | Site Contact Details Complete |
| Rule Description | Confirms site contact name, email, and mobile number are all provided. |
| Pass Criteria | 1. Site contact name provided.<br>2. Email provided.<br>3. Mobile number provided. |
| Validation Type | Base |
| Failed Action | One or more contact details missing. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C9 — Summary/Design Matches Order Form

| Field | Details |
|---|---|
| Validation Name | Summary/Design Matches Order Form |
| Rule Description | Confirms the order summary or design description is consistent with the design and order form documents attached. |
| Pass Criteria | 1. Summary/design content matches the attached design and order form. |
| Validation Type | Base |
| Failed Action | Mismatch between summary/design and attached documents. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C10 — Correct Billing Account/Company Name

| Field | Details |
|---|---|
| Validation Name | Correct Billing Account/Company Name |
| Rule Description | Confirms the order is associated with the correct customer account/company name to ensure accurate billing. |
| Pass Criteria | 1. Customer account/company name on the order matches the intended billing entity. |
| Validation Type | Base |
| Failed Action | Order on incorrect account/company name; billing would be wrong. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C11 — Customer LAN IP Details Provided (DIA)

| Field | Details |
|---|---|
| Validation Name | Customer LAN IP Details Provided (DIA) |
| Rule Description | For DIA (Direct Internet Access) orders, confirms the customer's LAN IP details have been provided. |
| Pass Criteria | 1. LAN IP details present for the DIA order. |
| Validation Type | Conditional — DIA orders only |
| Failed Action | LAN IP details missing for a DIA order. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C12 — Public IP Address Range Approved

| Field | Details |
|---|---|
| Validation Name | Public IP Address Range Approved |
| Rule Description | Where the customer has requested public IP address range(s), confirms that the request has been approved. |
| Pass Criteria | 1. If public IP ranges are requested, approval is documented. |
| Validation Type | Conditional — only applies when public IP ranges are requested |
| Failed Action | Public IP range requested but approval not documented. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C13 — IP Address Range Within Standard Offering

| Field | Details |
|---|---|
| Validation Name | IP Address Range Within Standard Offering |
| Rule Description | Confirms that any IP address range requested is within the standard offering (/30), flagging requests that exceed it. |
| Pass Criteria | 1. Requested IP range is /30 or within the standard offering. |
| Validation Type | Conditional — only applies when the customer requests an IP address range |
| Failed Action | Requested range exceeds the standard /30 offering; requires approval/escalation. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C14 — Kit, Router Compatibility & Fulfilment Correct

| Field | Details |
|---|---|
| Validation Name | Kit, Router Compatibility & Fulfilment Correct |
| Rule Description | Confirms the kit ordered is correct, the router is compatible with the product ordered, and the fulfilment method (run rate stock or ship-back) is correctly specified. *(This check currently bundles three distinct conditions — worth splitting into three separate checks so a failure identifies exactly which part failed.)* |
| Pass Criteria | 1. Kit is correct for the product.<br>2. Router is compatible with the product ordered.<br>3. Fulfilment run rate/ship-back is correctly specified. |
| Validation Type | Base |
| Failed Action | Kit incorrect, router incompatible, or fulfilment method incorrect — specify which. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C15 — Accessories & Licences Complete

| Field | Details |
|---|---|
| Validation Name | Accessories & Licences Complete |
| Rule Description | Confirms all required accessories (power supplies, antennas, extension cables) and licences requested are included on the order. |
| Pass Criteria | 1. Power supplies included if required.<br>2. Antennas included if required.<br>3. Extension cables included if required.<br>4. Licences included if required. |
| Validation Type | Base |
| Failed Action | One or more required accessories/licences missing from the order. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C16 — Third-Party Installation Included in Quote

| Field | Details |
|---|---|
| Validation Name | Third-Party Installation Included in Quote |
| Rule Description | Where third-party installation is required, confirms it is included in the quote. |
| Pass Criteria | 1. If installation is required, it is included in the quote. |
| Validation Type | Conditional — only applies when 3rd-party installation is required |
| Failed Action | Installation required but not included in the quote. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C17 — Contract Term Matches Order

| Field | Details |
|---|---|
| Validation Name | Contract Term Matches Order |
| Rule Description | Confirms the contract term is provided and matches what is specified on the order. |
| Pass Criteria | 1. Contract term provided.<br>2. Term matches the order. |
| Validation Type | Base |
| Failed Action | Contract term missing or mismatched. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C18 — B-End Information Correct

| Field | Details |
|---|---|
| Validation Name | B-End Information Correct |
| Rule Description | Where B-End information is required, confirms it has been provided and is correct. |
| Pass Criteria | 1. If required, B-End information is filled out.<br>2. Information is correct. |
| Validation Type | Conditional — only applies when B-End information is required |
| Failed Action | B-End info required but missing or incorrect. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C19 — QoS (AF/EF %) Correct

| Field | Details |
|---|---|
| Validation Name | QoS (AF/EF %) Correct |
| Rule Description | Where Quality of Service is required, confirms the AF and EF percentages are filled out on the order form and are correct. |
| Pass Criteria | 1. If QoS is required, AF % provided.<br>2. EF % provided.<br>3. Values are correct. |
| Validation Type | Conditional — only applies when QoS is required |
| Failed Action | QoS required but AF/EF % missing or incorrect. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C20 — Cease Details Included (If Applicable)

| Field | Details |
|---|---|
| Validation Name | Cease Details Included (If Applicable) |
| Rule Description | Where an existing service is to be ceased once the new service is complete, confirms cease details have been added to the request. |
| Pass Criteria | 1. If a cease is required, cease details are included in the request. |
| Validation Type | Conditional — only applies when a cease is required |
| Failed Action | Cease required but details missing from the request. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C21 — Upgrade/Downgrade Clearly Stated

| Field | Details |
|---|---|
| Validation Name | Upgrade/Downgrade Clearly Stated |
| Rule Description | Where the order is an upgrade or downgrade, confirms this is clearly stated on the order. |
| Pass Criteria | 1. If the order is an upgrade/downgrade, this is explicitly stated. |
| Validation Type | Conditional — only applies when the order is an upgrade/downgrade |
| Failed Action | Upgrade/downgrade not clearly stated on the order. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C22 — Referenced Email/File Attached

| Field | Details |
|---|---|
| Validation Name | Referenced Email/File Attached |
| Rule Description | Where comments reference a specific email or file, confirms that the referenced item is attached. |
| Pass Criteria | 1. If a comment references an email/file, that item is attached. |
| Validation Type | Conditional — only applies when a comment references an external email/file |
| Failed Action | Referenced email/file not attached. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C23 — Vendor Quote Still Valid

| Field | Details |
|---|---|
| Validation Name | Vendor Quote Still Valid |
| Rule Description | Confirms the vendor quote attached has not expired. |
| Pass Criteria | 1. Vendor quote date is within its validity period. |
| Validation Type | Base |
| Failed Action | Vendor quote expired; a current quote must be obtained. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C24 — Vodafone Quote to Customer Attached

| Field | Details |
|---|---|
| Validation Name | Vodafone Quote to Customer Attached |
| Rule Description | Confirms the Vodafone quote issued to the customer is attached. |
| Pass Criteria | 1. VF customer quote is attached. |
| Validation Type | Base |
| Failed Action | VF quote to customer missing. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C25 — Customer-Communicated Leadtime Captured

| Field | Details |
|---|---|
| Validation Name | Customer-Communicated Leadtime Captured |
| Rule Description | Captures and confirms what leadtime, if any, has been communicated to the customer. |
| Pass Criteria | 1. Leadtime communicated to the customer (if any) is documented. |
| Validation Type | Base |
| Failed Action | Leadtime communication not documented. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C26 — Vendor Quotations Attached

| Field | Details |
|---|---|
| Validation Name | Vendor Quotations Attached |
| Rule Description | Confirms vendor quotations are attached to the order. |
| Pass Criteria | 1. Vendor quotation(s) attached. |
| Validation Type | Base |
| Failed Action | Vendor quotation missing. |
| Status | Developed |

*Examples/screenshots: to be added.*

### C27 — Commercial Approval Included in Tech Spec

| Field | Details |
|---|---|
| Validation Name | Commercial Approval Included in Tech Spec |
| Rule Description | Confirms the tech spec includes evidence of commercial approval, including margin, via pricing tool output, EDRA, or a commercial manager email. |
| Pass Criteria | 1. Commercial approval evidence present (pricing tool, EDRA, or commercial manager email).<br>2. Margin included. |
| Validation Type | Base |
| Failed Action | Commercial approval or margin evidence missing from the tech spec. |
| Status | Developed |

*Examples/screenshots: to be added.*

---

## BSP Checks

### B1 — Customer Name Exists & Matches in BSP

| Field | Details |
|---|---|
| Validation Name | Customer Name Exists & Matches in BSP |
| Rule Description | Validates that the customer name provided in the tech spec or order form exactly matches the customer name record in BSP. |
| Pass Criteria | 1. Customer name exists in BSP.<br>2. Customer name matches exactly between tech spec/order form and BSP. |
| Validation Type | Base |
| Failed Action | Customer name does not exist in BSP, or does not match exactly. |
| Status | Developed |

**Additional Comments:** Where the customer name is not available in the system, a new customer record should be created via MDG. If the customer record exists but is inactive, it should be reactivated, or where required, a new record should be created through MDG.

*Examples/screenshots: to be added.*

### B2 — Delivery Address Exists in BSP

| Field | Details |
|---|---|
| Validation Name | Delivery Address Exists in BSP |
| Rule Description | Confirms the delivery address on the order exists as a record in BSP. |
| Pass Criteria | 1. Delivery address found in BSP. |
| Validation Type | Base |
| Failed Action | Delivery address not found in BSP. |
| Status | Developed |

**Additional Comments:** Raise with the BSP Team to create/correct the address record.

*Examples/screenshots: to be added.*

### B3 — Billing Entity Matches BSP Bill-To Name

| Field | Details |
|---|---|
| Validation Name | Billing Entity Matches BSP Bill-To Name |
| Rule Description | Confirms the billing entity name on the order matches the "bill_to_name" field in BSP. |
| Pass Criteria | 1. Billing entity name matches BSP bill_to_name exactly. |
| Validation Type | Base |
| Failed Action | Billing entity name mismatch. |
| Status | Developed |

**Additional Comments:** Raise via MDG.

*Examples/screenshots: to be added.*

### B4 — Opportunity Reference Matches VBOP

| Field | Details |
|---|---|
| Validation Name | Opportunity Reference Matches VBOP |
| Rule Description | Confirms the opportunity reference in the tech spec matches the corresponding record in VBOP. |
| Pass Criteria | 1. Opportunity ref in tech spec matches VBOP. |
| Validation Type | Base |
| Failed Action | Opportunity reference mismatch between tech spec and VBOP. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B5 — PO Number Consistent Across Sources

| Field | Details |
|---|---|
| Validation Name | PO Number Consistent Across Sources |
| Rule Description | Confirms the PO number is consistent across VBOP and the customer PO (or an email confirmation where a formal PO isn't available). |
| Pass Criteria | 1. PO number in VBOP matches the customer PO or confirmation email. |
| Validation Type | Base |
| Failed Action | PO number inconsistent across sources. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B6 — Vendor Cost Price Below Sell Price

| Field | Details |
|---|---|
| Validation Name | Vendor Cost Price Below Sell Price |
| Rule Description | Confirms the vendor PO cost price is lower than the sell price, comparing the Vodafone quote against the customer PO. |
| Pass Criteria | 1. Vendor cost price is less than the sell price. |
| Validation Type | Base |
| Failed Action | Vendor cost price is equal to or exceeds sell price; margin issue flagged. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B7 — Tech Spec Product Codes Present in Vendor Quote

| Field | Details |
|---|---|
| Validation Name | Tech Spec Product Codes Present in Vendor Quote |
| Rule Description | Confirms every product code listed in the tech spec is present in the vendor quote, or that the product name can otherwise be matched. |
| Pass Criteria | 1. Each tech spec product code is found in the vendor quote (by code or matched name). |
| Validation Type | Base |
| Failed Action | One or more product codes not found in the vendor quote. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B8 — Tech Spec Product Codes Exist in BSP (MDM)

| Field | Details |
|---|---|
| Validation Name | Tech Spec Product Codes Exist in BSP (MDM) |
| Rule Description | Confirms every product code in the tech spec exists in BSP via MDM. |
| Pass Criteria | 1. Each tech spec product code is found in BSP via MDM. |
| Validation Type | Base |
| Failed Action | Product code not found in BSP. |
| Status | Developed |

**Additional Comments:** Raise via MDM.

*Examples/screenshots: to be added.*

### B9 — Quantities Align Across Documents

| Field | Details |
|---|---|
| Validation Name | Quantities Align Across Documents |
| Rule Description | Confirms quantities are consistent across all order documents; the vendor quote quantity may be equal to or higher than the order, but not lower. |
| Pass Criteria | 1. Quantities match across documents, or the vendor quote quantity is equal to/higher than required. |
| Validation Type | Base |
| Failed Action | Quantity mismatch where the vendor quote is lower than required, or inconsistent across documents. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B10 — Vendor Quote Within 30-Day Validity

| Field | Details |
|---|---|
| Validation Name | Vendor Quote Within 30-Day Validity |
| Rule Description | Confirms the vendor quote is dated within the last 30 days and has not expired. |
| Pass Criteria | 1. Vendor quote date is within 30 days. |
| Validation Type | Base |
| Failed Action | Vendor quote is older than 30 days / expired. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B11 — Tech Spec Contact Details Complete

| Field | Details |
|---|---|
| Validation Name | Tech Spec Contact Details Complete |
| Rule Description | Confirms the contact name and details in the tech spec are fully completed. |
| Pass Criteria | 1. Contact name present.<br>2. Contact details (email/phone) present. |
| Validation Type | Base |
| Failed Action | Contact name or details missing/incomplete in the tech spec. |
| Status | Developed |

*Examples/screenshots: to be added.*

### B13 — Billing Address Present & Exists in BSP

| Field | Details |
|---|---|
| Validation Name | Billing Address Present & Exists in BSP |
| Rule Description | Confirms a billing address is present in the order documents and that it exists as a record in BSP. |
| Pass Criteria | 1. Billing address present in documents.<br>2. Billing address exists in BSP. |
| Validation Type | Base |
| Failed Action | Billing address missing from documents or not found in BSP. |
| Status | Developed |

**Additional Comments:** Raise with the BSP Team.

*Examples/screenshots: to be added.*

---

## Circuit Checks
*(Apply only to circuit orders.)*

### X1 — Contract Term Present (Circuit)

| Field | Details |
|---|---|
| Validation Name | Contract Term Present (Circuit) |
| Rule Description | Confirms the contract term is present on the circuit order form or tech spec. |
| Pass Criteria | 1. Contract term present. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Contract term missing. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X2 — Premise ID Present (SIRO)

| Field | Details |
|---|---|
| Validation Name | Premise ID Present (SIRO) |
| Rule Description | For SIRO vendor orders, confirms the Premise ID is present. |
| Pass Criteria | 1. If the vendor is SIRO, Premise ID is present. |
| Validation Type | Conditional — SIRO vendor orders only |
| Failed Action | Premise ID missing for a SIRO order. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X3 — Service Type Matches Supporting Docs

| Field | Details |
|---|---|
| Validation Name | Service Type Matches Supporting Docs |
| Rule Description | Confirms the service type is present and matches the supporting documentation. |
| Pass Criteria | 1. Service type present.<br>2. Matches supporting docs. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Service type missing or mismatched. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X4 — Speed Matches Customer Order Form

| Field | Details |
|---|---|
| Validation Name | Speed Matches Customer Order Form |
| Rule Description | Confirms the speed is present and matches the customer order form. |
| Pass Criteria | 1. Speed present.<br>2. Matches customer order form. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Speed missing or mismatched. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X5 — Product Name & Type Present

| Field | Details |
|---|---|
| Validation Name | Product Name & Type Present |
| Rule Description | Confirms both the product name and product type are present. |
| Pass Criteria | 1. Product name present.<br>2. Product type present. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Product name or type missing. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X6 — Service Address Matches BSP

| Field | Details |
|---|---|
| Validation Name | Service Address Matches BSP |
| Rule Description | Confirms the service address is present and matches the corresponding record in BSP. |
| Pass Criteria | 1. Service address present.<br>2. Matches BSP record. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Service address missing or mismatched. |
| Status | Developed |

**Additional Comments:** Raise with the BSP Team.

*Examples/screenshots: to be added.*

### X7 — Circuit Order Form PO Matches VBOP

| Field | Details |
|---|---|
| Validation Name | Circuit Order Form PO Matches VBOP |
| Rule Description | Confirms the PO number on the circuit order form matches VBOP. |
| Pass Criteria | 1. PO number matches VBOP. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | PO number mismatch. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X8 — Billing Frequency Present & Aligned

| Field | Details |
|---|---|
| Validation Name | Billing Frequency Present & Aligned |
| Rule Description | Confirms billing frequency is present and aligns with the order/contract terms. |
| Pass Criteria | 1. Billing frequency present.<br>2. Aligned with order. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | Billing frequency missing or misaligned. |
| Status | Developed |

*Examples/screenshots: to be added.*

### X9 — PO Type Set to Recurring

| Field | Details |
|---|---|
| Validation Name | PO Type Set to Recurring |
| Rule Description | Confirms the PO type field is set to "Recurring" for circuit orders. |
| Pass Criteria | 1. PO type = Recurring. |
| Validation Type | Conditional — circuit orders only |
| Failed Action | PO type not set to Recurring. |
| Status | Developed |

*Examples/screenshots: to be added.*
