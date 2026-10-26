# Project 09 — Form Fortress: Build a Sign-Up Page That Says “No”

**Track:** Web Security 101  
**Type:** Coding (Python + HTML/JS)  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

Websites must check what people type, just like a bouncer checks IDs at the
door. Browser-side checks are a friendly first filter, but an attacker can skip
them. The real guard has to stand on the server. This project builds both so
you can see the difference.

## What the code does

`form_fortress.py` starts a local sign-up page with:

- client-side HTML attributes and JavaScript messages,
- server-side checks for name, email, password strength, and confirmation,
- rejected values re-displayed safely with `html.escape`,
- a success page that explicitly says **no account was created**,
- a `--demo` mode that runs the server-side rules against five test cases.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\web-security-101\09-form-fortress"

# Start the local form
py -3 form_fortress.py

# Then open http://127.0.0.1:8000

# Test the validation rules without a browser
py -3 form_fortress.py --demo
```

Try these fake sign-ups:

| Name | Email | Password | Result |
|---|---|---|---|
| Ada Lovelace | `ada@example.com` | `Blue-Coffee-Rocket-42!` | accepted |
| Ada | `bad-email` | `password123` | rejected |
| Ada Lovelace | `ada@example.com` | `short` | rejected |
| Ada Lovelace | `ada@example.com` | `Blue-Coffee-Rocket-42!` twice | accepted |

## Experiments to try

1. Open DevTools and delete the `required` attributes from the HTML. Does the
   server still reject bad input? Why is that the important part?
2. Try a name containing `<script>alert(1)</script>`. What happens on the error
   page? Find the `html.escape` call that prevents it from running.
3. Add a maximum length to the password field in HTML, then send a longer
   password with a tool such as `curl`. Does the server still accept it?
4. Add one new rule: reject email addresses containing the word `spam`.
5. Write down three protections a real sign-up system needs that this demo
   deliberately leaves out (HTTPS, rate limiting, CSRF tokens, secure password
   hashing, email verification).

## What you learn

- Input validation and why “never trust the client” matters.
- Client-side vs. server-side enforcement.
- Output escaping as a defense against script injection.

## Safety

This app listens on `127.0.0.1` only, stores nothing, and creates no accounts.
Use fake details. Do not reuse this code as a real authentication system.
