/**
 * ==============================================================================
 * KARTHIK VENKATA JAYA KARTHIK — DEVELOPER PORTFOLIO
 * Core JavaScript: Sticky Header, ScrollSpy, Project Modals, Resume Viewer,
 * Copy Handlers, Real Contact Form Dispatch (Formspree / EmailJS / Mailto Fallback).
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollProgress();
  initNavbar();
  initScrollSpy();
  initScrollAnimations();
  initDeveloperCodeCopy();
  initProjectModals();
  initResumeModal();
  initClipboardActions();
  initContactForm();
  initDynamicYear();
});

/* ==========================================================================
   1. Scroll Progress Bar
   ========================================================================== */
function initScrollProgress() {
  const progressBar = document.getElementById('scroll-progress');
  if (!progressBar) return;

  const updateProgress = () => {
    const scrollPx = document.documentElement.scrollTop || document.body.scrollTop;
    const winHeightPx = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    if (winHeightPx <= 0) return;
    const scrolled = (scrollPx / winHeightPx) * 100;
    progressBar.style.width = `${scrolled}%`;
  };

  window.addEventListener('scroll', updateProgress, { passive: true });
}

/* ==========================================================================
   2. Sticky Navbar & Mobile Drawer
   ========================================================================== */
function initNavbar() {
  const header = document.getElementById('main-header');
  const toggleBtn = document.getElementById('mobile-toggle');
  const closeBtn = document.getElementById('mobile-close');
  const drawer = document.getElementById('mobile-drawer');
  const overlay = document.getElementById('mobile-overlay');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  const onScroll = () => {
    if (window.scrollY > 20) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  const openDrawer = () => {
    drawer?.classList.add('open');
    overlay?.classList.add('open');
    document.body.style.overflow = 'hidden';
    toggleBtn?.setAttribute('aria-expanded', 'true');
    drawer?.setAttribute('aria-hidden', 'false');
  };

  const closeDrawer = () => {
    drawer?.classList.remove('open');
    overlay?.classList.remove('open');
    document.body.style.overflow = '';
    toggleBtn?.setAttribute('aria-expanded', 'false');
    drawer?.setAttribute('aria-hidden', 'true');
  };

  toggleBtn?.addEventListener('click', openDrawer);
  closeBtn?.addEventListener('click', closeDrawer);
  overlay?.addEventListener('click', closeDrawer);

  mobileLinks.forEach(link => {
    link.addEventListener('click', closeDrawer);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer?.classList.contains('open')) {
      closeDrawer();
    }
  });
}

/* ==========================================================================
   3. ScrollSpy Active Nav Link Highlight
   ========================================================================== */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const desktopLinks = document.querySelectorAll('.nav-desktop-menu .nav-link');
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');

  const onScroll = () => {
    const scrollY = window.scrollY;

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 140;
      const sectionHeight = section.offsetHeight;
      const sectionId = section.getAttribute('id');

      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        desktopLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${sectionId}`);
        });
        mobileLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === `#${sectionId}`);
        });
      }
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
}

/* ==========================================================================
   4. Scroll Reveal Animations (Intersection Observer)
   ========================================================================== */
function initScrollAnimations() {
  const animElements = document.querySelectorAll('.fade-in-up');

  if (!('IntersectionObserver' in window)) {
    animElements.forEach(el => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -25px 0px'
  });

  animElements.forEach(el => observer.observe(el));
}

/* ==========================================================================
   5. Developer Snippet Copy Button
   ========================================================================== */
function initDeveloperCodeCopy() {
  const btn = document.getElementById('code-snippet-copy');
  if (!btn) return;

  const snippet = `const candidateProfile = {
  name: "Karthik Venkata Jaya Karthik",
  role: "Aspiring Software Developer",
  education: {
    institution: "Aditya Polytechnic College",
    branch: "Computer Science Engineering",
    cgpa: 9.72 // Top academic tier
  },
  coreSkills: ["Python", "FastAPI", "Java", "MySQL", "JavaScript", "AI APIs"],
  focusArea: "Practical Software & Scalable Web",
  availableForWork: true,
  workEthic: "Disciplined, pragmatic & continuous learner"
};`;

  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(snippet).then(() => {
      const original = btn.innerHTML;
      btn.innerHTML = `<i class="fa-solid fa-check" style="color: #34D399;"></i>`;
      setTimeout(() => {
        btn.innerHTML = original;
      }, 2000);
    });
  });
}

/* ==========================================================================
   6. Project Case Studies & Project Modals
   ========================================================================== */
const PROJECT_CASE_STUDIES = {
  weather: {
    title: 'Weather Application',
    tagline: 'REST API Integration • Real-Time Meteorological Web Application',
    overview: 'A responsive real-time weather application developed to provide meteorological telemetry (temperature, weather conditions, humidity, wind velocity, and atmospheric pressure) through a clean, low-latency user interface.',
    problem: 'Many meteorological interfaces are heavily cluttered with intrusive advertisements, slow loading times, and confusing navigational layouts, making quick weather checks on mobile devices frustrating.',
    solution: 'Designed and built a streamlined web application that queries live weather data from a reliable REST API, processes JSON payloads asynchronously, and renders clean metric cards optimized for instant readability.',
    features: [
      'Real-time city search with automatic coordinate and weather parameter retrieval.',
      'Comprehensive atmospheric metrics: Temperature, Weather Condition Icon, Humidity %, Wind Speed (km/h), and Barometric Pressure.',
      'Asynchronous error handling for non-existent city queries and connection timeouts.',
      'Fast, mobile-first responsive layout tested across multiple screen resolutions.'
    ],
    tech: ['Python', 'RESTful Weather API', 'HTML5', 'CSS3', 'JavaScript', 'Bootstrap 5'],
    challenges: 'Handling asynchronous HTTP exceptions cleanly when users enter misspelled locations or when external rate limits occur. Resolved by implementing friendly inline UI feedback and query input sanitization.',
    learnings: 'Deepened practical knowledge of asynchronous JavaScript (`fetch`, `async/await`), JSON data extraction, API response modeling, and building resilient user interfaces.',
    github: 'https://github.com/Karthik04-karanam',
    liveKey: 'weather'
  },
  parlour: {
    title: 'Beauty Parlour Management & Booking Website',
    tagline: 'Business Solution • Service Catalog & Client Appointment Portal',
    overview: 'A full-featured responsive commercial website built for local salon businesses, featuring a structured service catalog, transparent pricing packages, customer testimonials, and an appointment booking workflow.',
    problem: 'Small salon businesses frequently depend on manual telephone calls and paper appointment records, leading to double bookings, customer uncertainty regarding prices, and lost scheduling opportunities.',
    solution: 'Engineered an accessible client-facing portal that clearly showcases service categories, tiered pricing, duration estimates, and an appointment booking workflow with client feedback displays.',
    features: [
      'Interactive service directory with categorized pricing tiers and treatment packages.',
      'Self-service appointment reservation form with date/time selection.',
      'Client testimonial showcase presenting genuine service feedback.',
      'Mobile-first responsive design utilizing Bootstrap and customized DOM event handling with jQuery.'
    ],
    tech: ['HTML5', 'CSS3', 'Bootstrap 5', 'JavaScript', 'jQuery', 'Responsive UI'],
    challenges: 'Ensuring seamless form accessibility and consistent visual alignment across various smartphone displays with varying aspect ratios. Overcame this with CSS Flexbox, CSS Grid, and responsive breakpoint testing.',
    learnings: 'Gained hands-on experience in converting commercial business requirements into user-friendly digital workflows, DOM event manipulation, and customer-centric UI/UX design.',
    github: 'https://github.com/Karthik04-karanam',
    liveKey: 'parlour'
  },
  aura: {
    title: 'AURAAI — AI Productivity Workspace',
    tagline: 'Full Stack Python • Unified Generative AI Developer Workspace',
    overview: 'A unified productivity workspace designed to bring conversational AI, prompt libraries, document analysis, goal tracking, and developer code generation into a single cohesive dark-themed environment.',
    problem: 'Developers and students commonly suffer from severe tab fragmentation—constantly switching between chat interfaces, note apps, code editors, and goal trackers, which disrupts focus and productivity.',
    solution: 'Built an all-in-one productivity suite with a high-throughput FastAPI backend handling generative AI API communications, paired with an ergonomic dark interface featuring modular panels for notes, chat, and coding.',
    features: [
      'FastAPI asynchronous backend with robust request schema validation and model routing.',
      'Multi-modal workspace featuring AI Chat, Goals, Document Analysis, and Code Generation.',
      'Prompt template library allowing developers to quickly execute and reuse high-value prompts.',
      'Streaming token UI optimization with syntax highlighting and low-latency interaction.'
    ],
    tech: ['Python', 'FastAPI', 'HTML5', 'CSS3', 'JavaScript', 'AI APIs (Gemini/GPT)', 'JSON'],
    challenges: 'Managing asynchronous model response streams without blocking the client thread or dropping tokens during prolonged generations. Solved by leveraging FastAPI async handlers and client-side chunk processing.',
    learnings: 'Mastered REST API architecture using FastAPI, prompt engineering integration, secure API credential handling, and complex state management in frontend environments.',
    github: 'https://github.com/Karthik04-karanam',
    liveKey: 'aura'
  }
};

function initProjectModals() {
  const modalOverlay = document.getElementById('project-modal');
  const modalBody = document.getElementById('modal-body');
  const modalClose = document.getElementById('modal-close');
  const triggerBtns = document.querySelectorAll('.quick-view-btn');
  const demoBtns = document.querySelectorAll('.project-demo-btn');

  if (!modalOverlay || !modalBody) return;

  const openModal = (projectKey) => {
    const data = PROJECT_CASE_STUDIES[projectKey];
    if (!data) return;

    const config = window.PORTFOLIO_CONFIG || {};
    const projectLinks = config.PROJECT_LINKS || {};
    const specificLink = projectLinks[data.liveKey] || {};
    const githubUrl = specificLink.github || data.github;
    const liveDemoUrl = specificLink.liveDemo || '';

    modalBody.innerHTML = `
      <div style="margin-bottom: 20px;">
        <span class="section-badge" style="font-size: 0.72rem; padding: 4px 12px; margin-bottom: 10px;">${data.tagline}</span>
        <h3 style="font-size: 1.55rem; color: var(--text-heading); font-weight: 800; margin-bottom: 8px;">${data.title}</h3>
        <p style="color: var(--text-body-bright); font-size: 0.95rem; line-height: 1.65;">${data.overview}</p>
      </div>

      <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; margin-bottom: 20px;">
        <div style="margin-bottom: 12px;">
          <h4 style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 4px;">Problem Statement</h4>
          <p style="font-size: 0.88rem; color: var(--text-body); line-height: 1.6;">${data.problem}</p>
        </div>
        <div>
          <h4 style="font-size: 0.8rem; font-family: var(--font-mono); color: #34D399; text-transform: uppercase; margin-bottom: 4px;">Implemented Solution</h4>
          <p style="font-size: 0.88rem; color: var(--text-body); line-height: 1.6;">${data.solution}</p>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h4 style="font-size: 0.92rem; color: var(--text-heading); font-weight: 700; margin-bottom: 10px;">Key Architectural Features</h4>
        <ul style="display: flex; flex-direction: column; gap: 8px; font-size: 0.88rem; color: var(--text-body);">
          ${data.features.map(item => `
            <li style="display: flex; gap: 10px;">
              <i class="fa-solid fa-check" style="color: var(--accent-cyan); margin-top: 4px;"></i>
              <span>${item}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <div style="margin-bottom: 20px;">
        <h4 style="font-size: 0.92rem; color: var(--text-heading); font-weight: 700; margin-bottom: 10px;">Engineering Challenges &amp; What I Learned</h4>
        <div style="font-size: 0.88rem; color: var(--text-body); line-height: 1.6; margin-bottom: 8px;">
          <strong style="color: var(--text-heading);">Challenge:</strong> ${data.challenges}
        </div>
        <div style="font-size: 0.88rem; color: var(--text-body); line-height: 1.6;">
          <strong style="color: var(--text-heading);">Key Takeaway:</strong> ${data.learnings}
        </div>
      </div>

      <div style="margin-bottom: 24px;">
        <h4 style="font-size: 0.88rem; font-family: var(--font-mono); color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">Technologies Used</h4>
        <div style="display: flex; flex-wrap: wrap; gap: 7px;">
          ${data.tech.map(t => `<span class="tech-pill">${t}</span>`).join('')}
        </div>
      </div>

      <div style="display: flex; flex-wrap: wrap; gap: 12px; padding-top: 18px; border-top: 1px solid var(--border-subtle);">
        <a href="${githubUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary">
          <i class="fa-brands fa-github mr-1"></i> View Code on GitHub
        </a>
        ${liveDemoUrl ? `
          <a href="${liveDemoUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-accent">
            <i class="fa-solid fa-arrow-up-right-from-square mr-1"></i> Open Live Demo
          </a>
        ` : `
          <button class="btn btn-sm btn-secondary modal-inline-demo-notice">
            <i class="fa-solid fa-desktop mr-1"></i> In-Portfolio Preview
          </button>
        `}
        <button class="btn btn-sm btn-outline modal-inline-close">
          Close
        </button>
      </div>
    `;

    modalOverlay.classList.add('open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    const inlineClose = modalBody.querySelector('.modal-inline-close');
    inlineClose?.addEventListener('click', closeModal);

    const demoNoticeBtn = modalBody.querySelector('.modal-inline-demo-notice');
    demoNoticeBtn?.addEventListener('click', () => {
      closeModal();
      const targetCard = document.getElementById(`project-card-${data.liveKey}`);
      targetCard?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  };

  const closeModal = () => {
    modalOverlay.classList.remove('open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  triggerBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-project');
      if (key) openModal(key);
    });
  });

  demoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-project');
      const config = window.PORTFOLIO_CONFIG || {};
      const specificLink = (config.PROJECT_LINKS && config.PROJECT_LINKS[key]) || {};
      if (specificLink.liveDemo) {
        window.open(specificLink.liveDemo, '_blank', 'noopener,noreferrer');
      } else {
        // Open Case study / interactive preview explanation
        openModal(key);
      }
    });
  });

  modalClose?.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('open')) {
      closeModal();
    }
  });
}

/* ==========================================================================
   7. Online Resume Modal
   ========================================================================== */
function initResumeModal() {
  const modalOverlay = document.getElementById('resume-modal');
  const modalClose = document.getElementById('resume-modal-close');
  const modalBody = document.getElementById('resume-modal-body');
  const triggerBtn = document.getElementById('cta-view-resume');

  if (!modalOverlay || !modalClose || !modalBody || !triggerBtn) return;

  const renderResumeContent = () => {
    modalBody.innerHTML = `
      <div style="border-bottom: 2px solid var(--accent-cyan); padding-bottom: 12px; margin-bottom: 20px;">
        <h2 style="font-size: 1.6rem; color: var(--text-heading); font-weight: 800;">Karthik Venkata Jaya Karthik</h2>
        <div style="font-size: 0.95rem; color: var(--accent-cyan); font-weight: 600; margin-top: 4px;">
          Aspiring Software Developer | Python | Web Development | AI
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 14px; font-size: 0.82rem; color: var(--text-muted); margin-top: 8px;">
          <span>📍 Rajahmundry, Andhra Pradesh, India</span>
          <span>✉️ <a href="mailto:karanamvenkatjaykarthik@gmail.com" style="color: var(--accent-cyan);">karanamvenkatjaykarthik@gmail.com</a></span>
          <span>🔗 <a href="https://linkedin.com/in/venkat-jay-karthik-karanam-098800404" target="_blank" style="color: var(--accent-cyan);">LinkedIn Profile</a></span>
          <span>💻 <a href="https://github.com/Karthik04-karanam" target="_blank" style="color: var(--accent-cyan);">GitHub</a></span>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="font-size: 1rem; color: var(--text-heading); font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
          Profile Summary
        </h3>
        <p style="font-size: 0.88rem; color: var(--text-body); line-height: 1.65;">
          Final-year Computer Science Engineering Diploma student (<strong>CGPA: 9.72/10</strong>) with strong technical proficiency in full-stack Python development, REST API engineering, modern web technologies, and database architecture. Hands-on experience building practical applications including meteorological platforms, AI-powered productivity workspaces, and commercial booking systems. Disciplined problem solver eager to contribute to innovative software engineering teams.
        </p>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="font-size: 1rem; color: var(--text-heading); font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
          Technical Skills
        </h3>
        <div style="display: grid; grid-template-columns: 140px 1fr; gap: 6px 12px; font-size: 0.86rem;">
          <strong style="color: var(--text-body-bright);">Programming:</strong>
          <span style="color: var(--text-body);">Python, Java, C, JavaScript (ES6+)</span>
          <strong style="color: var(--text-body-bright);">Web Development:</strong>
          <span style="color: var(--text-body);">HTML5, CSS3, Bootstrap 5, jQuery, Responsive Web Design</span>
          <strong style="color: var(--text-body-bright);">Backend &amp; APIs:</strong>
          <span style="color: var(--text-body);">FastAPI, RESTful APIs, Python Backend Architecture</span>
          <strong style="color: var(--text-body-bright);">Databases:</strong>
          <span style="color: var(--text-body);">MySQL, Relational Database Modeling</span>
          <strong style="color: var(--text-body-bright);">Libraries &amp; Data:</strong>
          <span style="color: var(--text-body);">NumPy, Pandas</span>
          <strong style="color: var(--text-body-bright);">Tools:</strong>
          <span style="color: var(--text-body);">Git, GitHub, VS Code</span>
          <strong style="color: var(--text-body-bright);">AI Tools:</strong>
          <span style="color: var(--text-body);">Google Gemini, ChatGPT, GitHub Copilot</span>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="font-size: 1rem; color: var(--text-heading); font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
          Education
        </h3>
        <div style="margin-bottom: 12px;">
          <div style="display: flex; justify-content: space-between; font-weight: 700; color: var(--text-heading); font-size: 0.92rem;">
            <span>Diploma in Computer Science Engineering (Final Year)</span>
            <span style="color: var(--accent-cyan); font-family: var(--font-mono);">CGPA: 9.72 / 10</span>
          </div>
          <div style="font-size: 0.84rem; color: var(--accent-cyan);">Aditya Polytechnic College (2024 – 2027)</div>
          <div style="font-size: 0.82rem; color: var(--text-body); margin-top: 2px;">Data Structures &amp; Algorithms, Python Programming, Database Management, Web Engineering.</div>
        </div>
        <div>
          <div style="display: flex; justify-content: space-between; font-weight: 700; color: var(--text-heading); font-size: 0.92rem;">
            <span>Secondary School Certificate (SSC)</span>
            <span style="color: var(--accent-cyan); font-family: var(--font-mono);">Score: 91.0%</span>
          </div>
          <div style="font-size: 0.84rem; color: var(--accent-cyan);">Chunilal Jajoo Rotary Municipal High School (2024)</div>
        </div>
      </div>

      <div style="margin-bottom: 20px;">
        <h3 style="font-size: 1rem; color: var(--text-heading); font-family: var(--font-mono); text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 4px;">
          Certifications
        </h3>
        <div style="font-size: 0.86rem; color: var(--text-body); margin-bottom: 6px;">
          • <strong style="color: var(--text-heading);">Full Stack Python Development</strong> — Anurag IT Solutions (2026)
        </div>
        <div style="font-size: 0.86rem; color: var(--text-body);">
          • <strong style="color: var(--text-heading);">Computer Fundamentals &amp; Office Automation</strong> — Rama Krishna Math (2025)
        </div>
      </div>
    `;
  };

  const openResumeModal = () => {
    renderResumeContent();
    modalOverlay.classList.add('open');
    modalOverlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  };

  const closeResumeModal = () => {
    modalOverlay.classList.remove('open');
    modalOverlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  triggerBtn.addEventListener('click', openResumeModal);
  modalClose.addEventListener('click', closeResumeModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeResumeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalOverlay.classList.contains('open')) {
      closeResumeModal();
    }
  });
}

/* ==========================================================================
   8. Clipboard Copy Handlers
   ========================================================================== */
function initClipboardActions() {
  const copyButtons = document.querySelectorAll('.copy-pill-btn[data-copy]');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const textToCopy = btn.getAttribute('data-copy');
      if (!textToCopy) return;

      const setCopiedState = () => {
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<i class="fa-solid fa-check"></i> <span>Copied!</span>`;
        btn.classList.add('copied');

        setTimeout(() => {
          btn.innerHTML = originalHtml;
          btn.classList.remove('copied');
        }, 2000);
      };

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(textToCopy).then(setCopiedState).catch(() => {
          fallbackCopy(textToCopy, setCopiedState);
        });
      } else {
        fallbackCopy(textToCopy, setCopiedState);
      }
    });
  });

  function fallbackCopy(text, callback) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.opacity = '0';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      if (callback) callback();
    } catch (err) {
      console.warn('Clipboard copy fallback error');
    }
    document.body.removeChild(textArea);
  }
}

/* ==========================================================================
   9. Contact Form — Real FastAPI Backend Integration (SQLite + SMTP)
   ========================================================================== */
function initContactForm() {
  const form = document.getElementById('contact-form');
  const feedback = document.getElementById('form-feedback');
  const submitBtn = document.getElementById('submit-btn');

  if (!form || !feedback || !submitBtn) return;

  const btnText = submitBtn.querySelector('.btn-text');
  const btnLoader = submitBtn.querySelector('.btn-loader');

  // Input references
  const nameInput = document.getElementById('form-name');
  const emailInput = document.getElementById('form-email');
  const subjectInput = document.getElementById('form-subject');
  const messageInput = document.getElementById('form-message');
  const gotchaInput = document.getElementById('form-gotcha');

  // Error spans
  const errorName = document.getElementById('error-name');
  const errorEmail = document.getElementById('error-email');
  const errorSubject = document.getElementById('error-subject');
  const errorMessage = document.getElementById('error-message');

  const clearErrors = () => {
    if (errorName) errorName.textContent = '';
    if (errorEmail) errorEmail.textContent = '';
    if (errorSubject) errorSubject.textContent = '';
    if (errorMessage) errorMessage.textContent = '';
  };

  let isSubmitting = false;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isSubmitting) return;

    clearErrors();
    feedback.style.display = 'none';

    const name = nameInput?.value.trim() || '';
    const email = emailInput?.value.trim() || '';
    const subject = subjectInput?.value.trim() || '';
    const message = messageInput?.value.trim() || '';
    const gotcha = gotchaInput?.value.trim() || '';

    // Field-level Validation
    let hasError = false;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!name || name.length < 2) {
      if (errorName) errorName.textContent = 'Please enter your full name (at least 2 characters).';
      hasError = true;
    }

    if (!email || !emailRegex.test(email)) {
      if (errorEmail) errorEmail.textContent = 'Please provide a valid email address.';
      hasError = true;
    }

    if (!subject || subject.length < 3) {
      if (errorSubject) errorSubject.textContent = 'Please provide a subject (at least 3 characters).';
      hasError = true;
    }

    if (!message || message.length < 10) {
      if (errorMessage) errorMessage.textContent = 'Please write a message of at least 10 characters.';
      hasError = true;
    }

    if (hasError) return;

    // Set Submitting State
    isSubmitting = true;
    submitBtn.disabled = true;
    if (btnText) btnText.style.display = 'none';
    if (btnLoader) btnLoader.style.display = 'inline-flex';

    const config = window.PORTFOLIO_CONFIG || {};
    const apiBaseUrl = (config.API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');
    const recipientEmail = config.EMAIL || 'karanamvenkatjaykarthik@gmail.com';

    const showSuccess = (msg) => {
      feedback.className = 'form-feedback success';
      feedback.textContent = msg;
      feedback.style.display = 'block';
      form.reset();
    };

    const showError = (msg) => {
      feedback.className = 'form-feedback error';
      feedback.innerHTML = msg;
      feedback.style.display = 'block';
    };

    const resetBtnState = () => {
      isSubmitting = false;
      submitBtn.disabled = false;
      if (btnText) btnText.style.display = 'inline-flex';
      if (btnLoader) btnLoader.style.display = 'none';
    };

    try {
      const endpoint = `${apiBaseUrl}/api/contact`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          email: email,
          subject: subject,
          message: message,
          _gotcha: gotcha || undefined
        })
      });

      const data = await response.json().catch(() => null);

      if (response.ok && data && data.status === 'success') {
        // Truthfully distinguish between email sent vs saved in database
        if (data.email_status === 'sent') {
          showSuccess("Your message has been sent successfully. Thank you for reaching out!");
        } else {
          showSuccess("Your message has been received and saved securely in our database. Thank you for reaching out!");
        }
      } else {
        // Handle server-side errors
        let errorMsg = "Something went wrong. Please try again or contact me directly.";
        if (response.status === 429) {
          errorMsg = (data && data.detail) || "Too many requests. Please wait a few minutes before trying again.";
        } else if (response.status === 422) {
          if (data && Array.isArray(data.detail) && data.detail.length > 0) {
            errorMsg = `Validation error: ${data.detail[0].msg}`;
          } else {
            errorMsg = "Please verify your input fields and try again.";
          }
        } else if (data && data.message) {
          errorMsg = data.message;
        } else if (data && data.detail) {
          errorMsg = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail);
        }
        showError(`${errorMsg} (Direct email: <a href="mailto:${recipientEmail}" style="color: var(--accent-cyan); text-decoration: underline;">${recipientEmail}</a>)`);
      }
    } catch (networkError) {
      console.error('API connection error:', networkError);
      showError(
        `Unable to reach the backend service at <code>${apiBaseUrl}</code>. ` +
        `Please ensure the FastAPI server is running, or contact me directly at <a href="mailto:${recipientEmail}" style="color: var(--accent-cyan); text-decoration: underline;">${recipientEmail}</a>.`
      );
    } finally {
      resetBtnState();
    }
  });
}

/* ==========================================================================
   10. Dynamic Copyright Year
   ========================================================================= */
function initDynamicYear() {
  const yearEl = document.getElementById('current-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
}
