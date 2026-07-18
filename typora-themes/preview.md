# Rosé Pine — theme preview

A single document that exercises every element the theme styles. Open it in Typora,
switch between **Rosé Pine**, **Moon**, and **Dawn** from the Themes menu, and watch
the whole palette move together.

## Typographic scale

# Heading 1 — soft, muted, all natural pine
## Heading 2 — faux fur and a bit of soho
### Heading 3 — iris
#### Heading 4 — foam
##### Heading 5 — gold
###### HEADING 6 — MUTED CAPS

Body text sets around 65 characters of comfortable line length. Inline styles: **bold
text**, *italic emphasis*, ~~struck through~~, `inline code`, a [hyperlink](https://rosepinetheme.com),
==highlighted== marks, and a keyboard hint like <kbd>Ctrl</kbd> + <kbd>K</kbd>.

> A blockquote holds a quiet thought against a low-highlight ground with an iris rail.
>
> > Nested one level deeper picks up the foam rail.

## Lists and tasks

1. Ordered item with a foam marker
2. Second item
   - Nested unordered, iris marker
   - Another nested item

- [x] Finished task (checked box in iris)
- [ ] Pending task
- [ ] Another pending task

## Code

Inline `const x = 42` reads in rose. A fenced block with syntax highlighting:

```go
// admission grant/cancel — the race the audit flagged
func (m *Manager) Admit(ctx context.Context) (*Ticket, int, error) {
    select {
    case res := <-tk.done:        // dispatcher granted a slot
        return res.ticket, res.waited, nil
    case <-ctx.Done():            // caller cancelled first
        m.cancelWaiting(tk)       // must drain a buffered grant here
        return nil, 0, ctx.Err()
    }
}
```

```python
def normalize(text: str) -> str:
    """Collapse blank runs, preserve two-space hard breaks."""
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
```

## Table

| Role family | Mid-level | Decision | Blocker |
|---|---:|---|---|
| A. Serving Platform | **6/10** | MAYBE | single-backend launch path |
| B. Reliability / Release | **7/10** | SHORTLIST | five repos lack CI |
| C. Runtime / Performance | **4/10** | NO | no GPU / vLLM |
| D. GPU / Kubernetes | **2/10** | NO | no pod ever scheduled |

## Math (if enabled in Typora preferences)

Inline: the paired overhead is $d_i = \text{TTFT}_{gateway,i} - \text{TTFT}_{direct,i}$.

$$
p_{95}(d) = +2.2075\ \text{ms} \quad (n = 630)
$$

---

That horizontal rule fades out at both ends. If every colour above feels like one family,
the theme is doing its job.
