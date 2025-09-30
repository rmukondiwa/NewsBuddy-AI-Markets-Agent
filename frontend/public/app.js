
// ---------- UI helpers ----------
function $(id){
   return document.getElementById(id);
}

const CHAT_API_URL = 'http://localhost:6003';

// shows "busy" state on a button/status, returns reset function
function setBusy(btnId, statusId, busyText="Working..."){
  const btn = $(btnId), st = $(statusId);
  if(!btn || !st) return () => {};
  const prev = { txt: btn.textContent, disabled: btn.disabled, st: st.textContent };
  btn.disabled = true; btn.textContent = "⏳ " + busyText;
  st.textContent = "Loading…";
  return () => { btn.disabled = false; btn.textContent = prev.txt; st.textContent = "Ready"; };
}

// display JSON nicely in a <pre> tag
function showJSON(elId, data){
  $(elId).textContent = JSON.stringify(data, null, 2);
}

// fetch wrapper with error handling
async function safeFetch(url, opts){
  const res = await fetch(url, opts);
  if(!res.ok){
    const body = await res.text().catch(()=> "");
    throw new Error(`${res.status} ${res.statusText}${body ? ": " + body : ""}`);
  }
  return res.json();
}

// quick notification popup
function toast(msg, isErr=false){
  const el = document.createElement("div");
  el.textContent = msg;
  el.style.cssText = `
    position: fixed; bottom: 18px; left: 50%; transform: translateX(-50%);
    background: ${isErr ? "#fee2e2" : "#ecfeff"}; color: ${isErr ? "#991b1b" : "#0c4a6e"};
    border: 1px solid ${isErr ? "#fecaca" : "#bae6fd"};
    padding: 10px 12px; border-radius: 10px; font-size: 13px; box-shadow: 0 6px 18px rgba(2,6,23,.15); z-index: 50;
  `;
  document.body.appendChild(el);
  setTimeout(()=> el.remove(), 1700);
}

// ---------- Basic endpoints ----------
async function checkHealth(){
  const done = setBusy("btnHealth", "healthStatus", "Checking");
  try {
    const data = await safeFetch(`${CHAT_API_URL}/health`);
    showJSON('healthOut', data);
  } catch (e) {
    showJSON('healthOut', { error: String(e) });
    toast("Health check failed", true);
  } finally { done(); }
}

// ---------- Chat ----------
function addBubble(role, text){
  // append a chat bubble to chat log
  const log = $('chatLog');
  const b = document.createElement('div');
  b.className = `bubble ${role === 'user' ? 'me' : 'ai'}`;
  b.innerHTML = `${escapeHTML(text)}<span class="time">${new Date().toLocaleTimeString()}</span>`;
  log.appendChild(b);
  log.scrollTop = log.scrollHeight;
}

// clear all chat bubbles
function clearChat(){
  $('chatLog').innerHTML = "";
}

// escape HTML for safe rendering
function escapeHTML(s){
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// send chat message to backend when Enter is pressed
async function submit(event){
  if (event.key === "Enter") {
    sendChat();
  }
}

// send chat message to backend and display reply
async function sendChat(){
  const input = $('chatInput');
  const msg = input.value.trim();
  input.value = "";
  addBubble('user', msg);

  const done = setBusy("btnChat", "chatStatus", "Thinking");
  try {
    const data = await safeFetch(`${CHAT_API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    addBubble('assistant', data.reply || "(no reply)");
  } catch (e) {
    addBubble('assistant', "⚠️ " + String(e));
    toast("Chat request failed", true);
  } finally { done(); }
}
