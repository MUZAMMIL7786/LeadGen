(function() {
  const PROJECT_ID = 'VF.DM.69cb577be9aebe38455e6747.QivSdvalkiO0zt8f';
  const VF_URL = 'https://general-runtime.voiceflow.com';
  const SESSION_ID = 'user_' + Math.random().toString(36).substring(7);

  let isChatOpen = false;

  function init() {
    const container = document.createElement('div');
    container.innerHTML = `
      <div id="chatbot-overlay"></div>
      <div id="chatbot-modal">
        <div id="chatbot-header">
          <div class="chatbot-logo">
            wakilz
          </div>
          <div class="chatbot-header-actions">
            <button class="chatbot-demo-btn">Get a demo</button>
            <button class="chatbot-icon-btn" id="chatbot-refresh" title="Restart Chat">↻</button>
            <button class="chatbot-icon-btn" id="chatbot-close" title="Close">✕</button>
          </div>
        </div>
        <div id="chatbot-messages"></div>
      </div>

      <div id="chatbot-dock">
        <div id="chatbot-avatar-dock">
          <img src="https://i.pravatar.cc/100?img=47" alt="Navi">
        </div>
        <div id="chatbot-input-container">
          <input type="text" id="chatbot-input" placeholder="Ask me anything...">
          <button id="chatbot-mic">🎙️</button>
        </div>
      </div>
    `;
    document.body.appendChild(container);
    
    bindEvents();
  }

  function bindEvents() {
    const input = document.getElementById('chatbot-input');
    const closeBtn = document.getElementById('chatbot-close');
    const refreshBtn = document.getElementById('chatbot-refresh');

    input.addEventListener('focus', () => {
      if (!isChatOpen) {
        openChat();
        if (document.getElementById('chatbot-messages').children.length === 0) {
          interact({ type: 'launch' });
        }
      }
    });

    input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && input.value.trim() !== '') {
        const text = input.value.trim();
        input.value = '';
        appendUserMessage(text);
        interact({ type: 'text', payload: text });
      }
    });

    closeBtn.addEventListener('click', closeChat);

    document.addEventListener('click', (e) => {
      if (isChatOpen) {
        const modal = document.getElementById('chatbot-modal');
        const dock = document.getElementById('chatbot-dock');
        if (modal && dock && !modal.contains(e.target) && !dock.contains(e.target)) {
          closeChat();
        }
      }
    });
    
    refreshBtn.addEventListener('click', () => {
      document.getElementById('chatbot-messages').innerHTML = '';
      interact({ type: 'launch' });
    });
  }

  function openChat() {
    isChatOpen = true;
    document.getElementById('chatbot-modal').classList.add('open');
    document.getElementById('chatbot-overlay').classList.add('open');
  }

  function closeChat() {
    isChatOpen = false;
    document.getElementById('chatbot-modal').classList.remove('open');
    document.getElementById('chatbot-overlay').classList.remove('open');
  }

  function scrollToBottom() {
    const msgs = document.getElementById('chatbot-messages');
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showTypingIndicator() {
    const msgs = document.getElementById('chatbot-messages');
    let typing = document.getElementById('chatbot-typing');
    if(!typing) {
      typing = document.createElement('div');
      typing.id = 'chatbot-typing';
      typing.className = 'chatbot-bot-card fade-in-msg';
      typing.innerHTML = `
        <div class="chatbot-bot-card-header">
          <img src="https://i.pravatar.cc/100?img=47" class="chatbot-bot-avatar" alt="Navi">
          <span class="chatbot-bot-name">Navi</span>
        </div>
        <div class="chatbot-bot-card-body typing-dots">
          <span>.</span><span>.</span><span>.</span>
        </div>
      `;
    }
    // Always append to move it to the end of the list
    msgs.appendChild(typing);
    typing.style.display = 'block';
    scrollToBottom();
  }

  function hideTypingIndicator() {
    const typing = document.getElementById('chatbot-typing');
    if(typing) typing.style.display = 'none';
  }

  function appendBotMessage(text) {
    const msgContainer = document.createElement('div');
    msgContainer.className = 'chatbot-bot-card fade-in-msg';
    
    // Parse bold markdown from text into html
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\\n/g, '<br>');

    msgContainer.innerHTML = `
      <div class="chatbot-bot-card-header">
        <img src="https://i.pravatar.cc/100?img=47" class="chatbot-bot-avatar" alt="Navi">
        <span class="chatbot-bot-name">Navi</span>
        <div class="chatbot-bot-actions">
          <button class="chatbot-action-btn" title="Copy">📋</button>
          <button class="chatbot-action-btn" title="Thumbs Up">👍</button>
          <button class="chatbot-action-btn" title="Thumbs Down">👎</button>
        </div>
      </div>
      <div class="chatbot-bot-card-body">
        ${formattedText}
      </div>
    `;
    
    const msgs = document.getElementById('chatbot-messages');
    const typing = document.getElementById('chatbot-typing');
    if(typing && typing.style.display !== 'none') {
      msgs.insertBefore(msgContainer, typing);
    } else {
      msgs.appendChild(msgContainer);
    }
    scrollToBottom();
  }

  function appendUserMessage(text) {
    const msgContainer = document.createElement('div');
    msgContainer.className = 'chatbot-user-msg fade-in-msg';
    msgContainer.innerText = text;
    
    const msgs = document.getElementById('chatbot-messages');
    msgs.appendChild(msgContainer);
    scrollToBottom();
  }

  function appendChoices(choices) {
    if (!choices || choices.length === 0) return;
    const btnsContainer = document.createElement('div');
    btnsContainer.className = 'chatbot-choices-container fade-in-msg';
    choices.forEach(c => {
      const btn = document.createElement('button');
      btn.className = 'chatbot-choice-btn';
      btn.innerText = c.name;
      btn.onclick = () => {
        appendUserMessage(c.name);
        interact({ type: 'text', payload: c.name });
        btnsContainer.style.display = 'none';
      };
      btnsContainer.appendChild(btn);
    });
    
    const msgs = document.getElementById('chatbot-messages');
    const typing = document.getElementById('chatbot-typing');
    if(typing && typing.style.display !== 'none') {
      msgs.insertBefore(btnsContainer, typing);
    } else {
      msgs.appendChild(btnsContainer);
    }
    scrollToBottom();
  }

  async function interact(request) {
    showTypingIndicator();
    
    try {
      const res = await fetch(`${VF_URL}/state/user/${SESSION_ID}/interact`, {
        method: 'POST',
        headers: {
          'Authorization': PROJECT_ID,
          'Content-Type': 'application/json',
          'versionID': 'development'
        },
        body: JSON.stringify({ action: request })
      });
      
      hideTypingIndicator();
      
      if (res.ok) {
        const traces = await res.json();
        traces.forEach(trace => {
          if (trace.type === 'text') {
            appendBotMessage(trace.payload.message);
          } else if (trace.type === 'choice') {
            appendChoices(trace.payload.buttons || trace.payload.choices);
          }
        });
      } else {
        console.error('Voiceflow API Error:', res.statusText);
      }
    } catch (err) {
      hideTypingIndicator();
      console.error('Fetch error:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
