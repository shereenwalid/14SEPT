"""View 3: Validation - exact markup from validationPage.html (sidebar removed,
buttons: Return to Order Entry + Proceed to Order Creation). Items rendered by JS."""


def view() -> str:
    return """
    <div id="view-validation" style="display:none;">
      <main class="flex-1 pt-4 p-4 md:px-6 md:pb-6 flex flex-col gap-4 mx-auto w-full" style="max-width:1400px; font-family:'Hanken Grotesk',sans-serif;">
        <header class="flex flex-col md:flex-row justify-between items-start md:items-end gap-3 border-b border-surface-variant pb-4 mt-2 md:mt-0 shrink-0">
          <div>
            <h2 class="text-[28px] font-bold text-on-background">Delivery Service Transition Acceptance Validation</h2>
            <p class="font-body-md text-sm text-secondary mt-1" id="val-opp-subtitle">Opportunity ID: -</p>
          </div>
          <div class="flex gap-2">
            <button onclick="resetToLanding()"
               class="px-4 py-1.5 bg-primary-container text-white font-button rounded hover:bg-primary transition-colors flex items-center gap-2 text-sm">
              <span class="material-symbols-outlined">keyboard_return</span>
              Return to Order Entry
            </button>
            <button id="proceed-btn" onclick="tryProceed()" disabled
               class="px-4 py-1.5 bg-gray-200 text-gray-400 font-button rounded cursor-not-allowed transition-colors flex items-center gap-2 text-sm">
              <span class="material-symbols-outlined">arrow_forward</span>
              Proceed to Order Creation
            </button>
          </div>
        </header>

        <div id="val-banner"></div>

        <div class="flex items-center gap-2 shrink-0">
          <span class="font-label-sm text-[10px] text-secondary uppercase tracking-wider">Order Category</span>
          <span id="val-order-category"
                class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-sidebar-dark text-white text-[10px] uppercase font-bold tracking-wider">
            <span class="material-symbols-outlined text-[13px]">category</span>
            <span id="val-order-category-text">-</span>
          </span>
        </div>

        <section class="bg-surface-container-lowest rounded-xl border border-surface-variant p-0 overflow-hidden flex flex-col shrink-0">
          <div class="bg-white p-3 border-b border-gray-200 shrink-0">
            <h3 class="text-[13px] leading-tight text-gray-500 font-semibold uppercase tracking-wider">Validation Checks</h3>
          </div>
          <div class="p-0 overflow-y-auto max-h-[640px]" style="scrollbar-width:thin; scrollbar-color:#b70100 #f3f3f3;">
            <div class="flex flex-col" id="val-groups"></div>
          </div>
        </section>

        <section class="bg-white rounded-xl border border-gray-200 p-0 overflow-hidden flex flex-col mt-3 shadow-sm">
          <div class="bg-white px-4 py-3 border-b border-gray-200 shrink-0 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-[18px]">flag</span>
              <h3 class="text-[13px] leading-tight text-gray-600 font-semibold uppercase tracking-wider">Raised Requests</h3>
            </div>
            <div class="flex items-center gap-3">
              <span id="val-feedbacks-count" class="text-[11px] text-gray-400 font-medium"></span>
              <button type="button" id="fb-add-btn" onclick="toggleNewRequest()"
                      title="Raise a request"
                      class="w-7 h-7 rounded-full bg-primary text-white flex items-center justify-center hover:bg-red-700 transition-colors shrink-0">
                <span class="material-symbols-outlined text-[18px]">add</span>
              </button>
            </div>
          </div>

          <!-- Inline form: raise a request against a failed check -->
          <div id="fb-new-form" style="display:none;" class="px-4 py-3 border-b border-gray-200 bg-gray-50">
            <div class="flex flex-col gap-2">
              <div>
                <label class="text-[11px] uppercase tracking-wider text-gray-500 font-semibold">Failed check</label>
                <input id="fb-new-search" type="text" autocomplete="off"
                       placeholder="Type to search failed checks..."
                       oninput="filterFailedChecks()"
                       class="mt-1 w-full border border-gray-300 rounded px-3 py-1.5 text-[13px] bg-white" />
                <select id="fb-new-check" size="5"
                        class="mt-1 w-full border border-gray-300 rounded px-2 py-1 text-[13px] bg-white"></select>
                <div id="fb-new-empty" class="text-[11px] text-gray-400 mt-1" style="display:none;">
                  No failed checks left without a request.
                </div>
              </div>
              <div class="flex flex-wrap items-center gap-2">
                <select id="fb-new-opt"
                        class="text-[12px] border border-gray-300 rounded px-3 py-1.5 bg-white min-w-[220px]"></select>
                <input id="fb-new-cmt" type="text" placeholder="Comment (optional)"
                       class="text-[12px] border border-gray-300 rounded px-3 py-1.5 bg-white flex-1 min-w-[200px]" />
                <button type="button" onclick="submitNewRequest()"
                        class="text-[11px] uppercase tracking-wider px-4 py-1.5 rounded bg-sidebar-dark text-white hover:bg-black"
                        style="font-family:'JetBrains Mono',monospace;">Save</button>
                <button type="button" onclick="toggleNewRequest(false)"
                        class="text-[11px] uppercase tracking-wider px-3 py-1.5 rounded border border-gray-300 text-gray-600 hover:bg-gray-100">Cancel</button>
                <span id="fb-new-status" class="text-[11px] text-secondary"></span>
              </div>
            </div>
          </div>
          <div class="p-0 overflow-y-auto max-h-[320px]" style="scrollbar-width:thin; scrollbar-color:#d1d5db #f3f3f3;">
            <ul class="flex flex-col" id="val-feedbacks-list"></ul>
          </div>
        </section>
      </main>
    </div>
    """
