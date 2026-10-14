/**
 * ==============================================================================
 * PORTFOLIO CLIENT CONFIGURATION
 * Karthik Venkata Jaya Karthik - Aspiring Software Developer
 * ==============================================================================
 * 
 * Central configuration file for frontend client-side services.
 */

window.PORTFOLIO_CONFIG = {
  // Candidate Profile Information
  NAME: 'Karthik Venkata Jaya Karthik',
  TITLE: 'Aspiring Software Developer | Python | Web Development | AI',
  EMAIL: 'karanamvenkatjaykarthik@gmail.com',
  LOCATION: 'Rajahmundry, Andhra Pradesh, India',

  // Social & Professional Profiles
  SOCIAL_LINKS: {
    github: 'https://github.com/Karthik04-karanam',
    linkedin: 'https://www.linkedin.com/in/venkat-jay-karthik-karanam-098800404',
    codechef: 'https://www.codechef.com/users/holy_care_25',
    email: 'mailto:karanamvenkatjaykarthik@gmail.com'
  },

  // Document Paths
  RESUME_PATH: 'assets/resume.pdf',
  RESUME_MD_PATH: 'assets/resume.md',

  /**
   * ============================================================================
   * BACKEND API CONFIGURATION (FastAPI + SQLite + SMTP)
   * ============================================================================
   * For local development, points to the local FastAPI Uvicorn server:
   *   'http://127.0.0.1:8000'
   * In production, update this to your deployed API domain:
   *   e.g. 'https://api.yourportfolio.com' or '' if frontend & backend share a domain.
   */
  API_BASE_URL: 'http://127.0.0.1:8000',

  /**
   * Project Live Demo Links
   */
  PROJECT_LINKS: {
    weather: {
      github: 'https://github.com/Karthik04-karanam',
      liveDemo: '' // e.g., 'https://karthik-weather.netlify.app'
    },
    parlour: {
      github: 'https://github.com/Karthik04-karanam',
      liveDemo: '' // e.g., 'https://karthik-parlour.netlify.app'
    },
    aura: {
      github: 'https://github.com/Karthik04-karanam',
      liveDemo: '' // e.g., 'https://karthik-aura.vercel.app'
    }
  }
};
