# Client Script API

Globals injected on every Cafe page via Builder settings global `client-script.js`.

---

## `toast(options)`

```js
toast(string | { title, text, icon, position, timeout })
// icon: "success" | "error" | "info" | "warning"
// position: "top-right" | "top-left" | "top-center" | "bottom-right" | "bottom-left" | "bottom-center" (default: "bottom-right")
// timeout: ms, default 5000, 0 = persistent

toast.success(text, options?)
toast.error(text, options?)
toast.info(text, options?)
toast.warning(text, options?)
```

---

## `dialog(options)` → `{ close() }`

```js
dialog({
  title,              // string
  message,            // plain text body
  html,               // raw HTML body
  error,              // error text (styled)
  size,               // "sm" | "md" | "lg" | "xl" | "2xl" (default: "md")
  onClose,            // () => void
  actions: [
    {
      label,          // string
      variant,        // "solid" | "default"
      theme,          // "red" | undefined
      onClick(close), // call close() to dismiss
    }
  ]
})
```

---

## `frappeClient`

All methods return `Promise`.

```js
// Fetch single doc or filtered list
frappeClient.get(doctype, name?, filters?)
frappeClient.getDoc(doctype, name, filters?)       // alias for get()

// Fetch list with pagination
frappeClient.getDocList(doctype, { filters, fields, limit=20, start=0 })
// filters: [["fieldname", "operator", value], ...]

// Document count
frappeClient.count(doctype, filters?)

// CRUD
frappeClient.post(doctype, data)
frappeClient.update(doctype, name, data)
frappeClient.delete(doctype, name)

// Field update shortcut
frappeClient.setValue(doctype, name, fieldname, value)

// Call whitelisted server method
frappeClient.call(method, args?, { useQuery? })    // useQuery=true → GET, default POST

// Run a doc-level whitelisted method
frappeClient.runDocMethod(doctype, name, method, args?)

// File upload
frappeClient.uploadFile(file, { private, folder, doctype, docname, fieldname, uploadEndpoint })

// Override CSRF token (auto-read from frappe.csrf_token)
frappeClient.setCSRFToken(token)
```
