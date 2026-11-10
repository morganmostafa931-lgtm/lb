# lb — Fiper Skills

مجموعة skills عامة لـ Claude Code لبناء صفحة الهبوط الخاصة بفايبر. تعمل في أي مشروع، ولا تعمل إلا عندما تستدعيها بنفسك.

| الأمر | ماذا يفعل |
|---|---|
| `/fiper-brand` | يعرض هوية فايبر (الألوان، الخطوط، النبرة، قواعد RTL) أو يحدّثها |
| `/fiper-landing-section [القسم]` | يبني أو يعدّل قسماً من الصفحة (hero، features، pricing، faq...) أو الصفحة كاملة |
| `/fiper-copywriting [النص المطلوب]` | يكتب أو يحسّن النصوص التسويقية بالعربية أو الإنجليزية |
| `/fiper-landing-review [الملف]` | يفحص الصفحة قبل النشر (الجوال، RTL، الوصولية، SEO، الأداء) |

## التثبيت (مرة واحدة على جهازك)

```bash
git clone https://github.com/morganmostafa931-lgtm/lb.git
cd lb
./install.sh
```

يضع السكربت الـ skills في `~/.claude/skills/`، فتصبح متاحة في كل مشاريعك. للتحديث لاحقاً شغّل `git pull && ./install.sh`.

## قبل أول استخدام

افتح `skills/fiper-brand/SKILL.md` واملأ قيم `TODO`: وصف المنتج، الجمهور، الألوان، الخطوط، الشعار. يمكنك أيضاً أن تكتب مثلاً:

```
/fiper-brand اللون الأساسي #7C3AED والخط Cairo
```

مثال للاستخدام:

```
/fiper-landing-section ابنِ قسم الـ hero والمميزات
/fiper-landing-review index.html
```
