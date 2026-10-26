# Project 08 — Cookie Trail: What Websites Remember About You

**Track:** Web Security 101  
**Type:** Coding (Python)  
**Time:** ~40 minutes  
**Difficulty:** Beginner

## The concept

Cookies are little name tags a website gives your browser so it can recognize
you next time — like a coat-check ticket. Some keep you logged in, some store
preferences, and some are used to follow you around. Safety flags such as
`HttpOnly`, `Secure`, and `SameSite` control how those cookies can be used.

## What the code does

`cookie_lab.py` runs a tiny website on `127.0.0.1` that sets four cookies:

| Cookie | Flags | Lesson |
|---|---|---|
| `session_id` | `HttpOnly`, `SameSite=Lax` | JavaScript cannot read it |
| `theme` | `Max-Age`, `SameSite=Lax` | Preferences can expire |
| `unsafe_pref` | none | Visible to JavaScript |
| `secure_demo` | `Secure`, `SameSite=None` | Only for HTTPS connections |

The page includes a JavaScript panel that shows what `document.cookie` can see,
and a server view that shows what the server receives. A separate `--demo`
prints the raw `Set-Cookie` headers automatically.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\web-security-101\08-cookie-trail"

# Start the local lab
py -3 cookie_lab.py

# Then open http://127.0.0.1:8000 in your browser

# Or run the automated demo, no browser needed
py -3 cookie_lab.py --demo
```

In the browser:

1. Click **Set the demo cookies**.
2. Open DevTools → **Application** (Chrome/Edge) or **Storage** (Firefox).
3. Find **Cookies** → `http://127.0.0.1:8000`.
4. Compare the flags with the JavaScript panel and the **Server view**.
5. Click **Log out / clear** and watch the cookies expire.

## Experiments to try

1. Which cookies can JavaScript read? Which can it not read?
2. Does the server still receive the `HttpOnly` cookie? Why?
3. Why is `Secure` useless on a plain HTTP site?
4. Change `SameSite=Lax` to `SameSite=Strict` in the code and predict what
   changes when you click a link from another site.
5. Count the third-party cookies on a news site you use. How many are there?

## What you learn

- Cookies, sessions, and browser storage.
- The purpose of `HttpOnly`, `Secure`, and `SameSite`.
- How tracking works at a basic level, and how to reduce it.

## Safety

The server binds to `127.0.0.1` only, uses random fake IDs, and stores nothing.
It is not a real authentication system. Only inspect cookies in your own
browser; do not tamper with other people’s sessions.
