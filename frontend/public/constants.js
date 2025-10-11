// Auto-switch based on hostname
const BACKEND_URLS = {
  local: "http://localhost:6003",
  vm: "http://vcm-49714.vm.duke.edu:6003",
  prod: "https://dumb-prod-domain.com"
};

window.CHAT_API_URL =
  window.location.hostname.includes("localhost")
    ? BACKEND_URLS.local
    : window.location.hostname.includes("vcm-49714.vm.duke.edu")
    ? BACKEND_URLS.vm
    : BACKEND_URLS.prod;