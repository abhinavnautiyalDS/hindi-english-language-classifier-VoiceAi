# Mixed-Script Code-Mixing Policy

The project's `LANGUAGE-English` categories mean **mixed script in one utterance**, not merely two languages typed in one script.

| Category | Required native script + Latin English | Label |
|---|---|---|
| Hindi-English / Hinglish | Devanagari + Latin | `hi-IN` |
| Punjabi-English | Gurmukhi + Latin | `pa-IN` |
| Bengali-English | Bengali + Latin | `bn-IN` |
| Gujarati-English | Gujarati + Latin | `gu-IN` |
| Kannada-English | Kannada + Latin | `kn-IN` |
| Malayalam-English | Malayalam + Latin | `ml-IN` |
| Marathi-English | Devanagari + Latin | `mr-IN` |
| Telugu-English | Telugu + Latin | `te-IN` |
| Assamese-English | Assamese + Latin | `as-IN` |
| Tamil-English | Tamil + Latin | `ta-IN` |

## Accept only after both stages

1. **Mechanical gate:** at least one character in the category's native Unicode script range AND at least one Latin letter appear in the same text.
2. **Language review:** confirm both languages are genuinely used. Reject cases where the Latin segment is only a brand, URL, acronym, or a single incidental borrowed token.

Script heuristics are not language identification. In particular, Bengali and Assamese script ranges overlap; a human/source-informed language check must disambiguate them. Romanized language-English text entirely in Latin script does not qualify for these mixed-script categories under this project requirement.

The language-only categories have their own source/script rules. This gate applies to language-English categories only.
