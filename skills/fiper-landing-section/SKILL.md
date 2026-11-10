---
name: fiper-landing-section
disable-model-invocation: true
argument-hint: "[وصف ما تريد]"
description: بناء أو تعديل قسم في صفحة الهبوط الخاصة بفايبر (Hero، المميزات، طريقة العمل، الأسعار، آراء العملاء، الأسئلة الشائعة، CTA، Footer). Build or edit a section of the Fiper landing page — hero, features, how-it-works, pricing, testimonials, FAQ, CTA, footer — responsive, RTL-first and accessible.
---

# بناء أقسام صفحة الهبوط لفايبر

## طلب المستخدم

$ARGUMENTS

إذا لم يحدد المستخدم القسم المطلوب، فاسأله: أي قسم تريد، أم الصفحة كاملة؟

## قبل أن تبدأ

1. اقرأ الملف `../fiper-brand/SKILL.md` (بالنسبة لمجلد هذه الـ skill)، ففيه الألوان والخطوط والنبرة. لا تبدأ قبل قراءته.
2. افحص المشروع لتعرف الـ stack المستخدم (`package.json` أو `index.html` أو غيرهما) والتزم به.
   إذا كان المشروع فارغاً فالافتراضي هو **HTML + CSS + JS بسيط بدون build**، وهيكله:
   ```
   index.html
   assets/css/styles.css
   assets/js/main.js
   assets/img/
   ```
3. إذا احتاج القسم نصوصاً تسويقية، فاكتبها حسب الملف `../fiper-copywriting/SKILL.md` (بالنسبة لمجلد هذه الـ skill).

## ترتيب الأقسام الافتراضي

| # | القسم | `id` | الهدف |
|---|---|---|---|
| 1 | Header / Nav | `top` | الشعار، روابط الأقسام، زر CTA |
| 2 | Hero | `hero` | الوعد الأساسي وCTA رئيسي، ويظهر قبل التمرير |
| 3 | Social proof | `trust` | شعارات عملاء أو أرقام (حقيقية فقط) |
| 4 | المشكلة ← الحل | `problem` | لماذا يحتاج الزائر فايبر |
| 5 | المميزات | `features` | من 3 إلى 6 مميزات، كل ميزة بفائدتها |
| 6 | طريقة العمل | `how` | 3 خطوات مرقّمة |
| 7 | آراء العملاء | `testimonials` | اقتباسات حقيقية فقط |
| 8 | الأسعار | `pricing` | الخطط، مع تمييز الخطة الموصى بها |
| 9 | الأسئلة الشائعة | `faq` | من 5 إلى 8 أسئلة باستخدام `<details>` |
| 10 | CTA ختامي | `cta` | تكرار الإجراء الرئيسي |
| 11 | Footer | `footer` | روابط، تواصل، حقوق |

يمكن حذف قسم أو تغيير ترتيبه حسب طلب المستخدم، لكن Hero يبقى أولاً وCTA الختامي يبقى قبل Footer.

## قواعد كل قسم

- غلّف كل قسم بـ `<section id="..." aria-labelledby="...-title">` وأعطه عنوان `<h2 id="...-title">`.
  في الصفحة `<h1>` واحد فقط، وهو في Hero.
- التصميم Mobile-first: ابدأ بعمود واحد، ثم استخدم `@media (min-width: 768px)` و`(min-width: 1024px)`.
- لا تسمح بأي تمرير أفقي، واجعل الهامش الجانبي 16px على الأقل في الجوال.
- أقصى عرض للمحتوى `1200px` مع `margin-inline: auto`.
- استخدم متغيرات الألوان `var(--fiper-*)` فقط، والخصائص المنطقية `*-inline-*` بدل left/right.
- الصور: اكتب `alt` وصفياً، وحدّد `width` و`height`، واستخدم `loading="lazy"` لكل صورة تحت Hero.
  صورة Hero تأخذ `fetchpriority="high"` وليس `lazy`.
- الأزرار والروابط: لا تقل مساحة النقر عن 44×44px، واجعل `:focus-visible` ظاهراً.
- الحركة: انتقالات بسيطة فقط، واحترم `@media (prefers-reduced-motion: reduce)`.

## قوالب سريعة

### Hero
```html
<section id="hero" class="hero" aria-labelledby="hero-title">
  <div class="container hero__inner">
    <div class="hero__text">
      <h1 id="hero-title">[الوعد الأساسي في جملة واحدة]</h1>
      <p class="hero__sub">[جملة توضح لمن المنتج وما الفائدة]</p>
      <div class="hero__actions">
        <a href="#cta" class="btn btn--primary">[CTA رئيسي]</a>
        <a href="#how" class="btn btn--ghost">[CTA ثانوي]</a>
      </div>
    </div>
    <img src="assets/img/hero.webp" alt="[وصف الصورة]" width="640" height="480" fetchpriority="high">
  </div>
</section>
```

### المميزات
```html
<section id="features" aria-labelledby="features-title">
  <div class="container">
    <h2 id="features-title">[عنوان المميزات]</h2>
    <ul class="features-grid" role="list">
      <li class="feature-card">
        <svg aria-hidden="true" ...></svg>
        <h3>[اسم الميزة]</h3>
        <p>[الفائدة للزائر]</p>
      </li>
    </ul>
  </div>
</section>
```
```css
.features-grid { display: grid; gap: 24px; grid-template-columns: 1fr; list-style: none; padding: 0; }
@media (min-width: 768px)  { .features-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .features-grid { grid-template-columns: repeat(3, 1fr); } }
```

### الأسئلة الشائعة (بدون JavaScript)
```html
<details class="faq-item">
  <summary>[السؤال]</summary>
  <p>[الجواب]</p>
</details>
```

## بعد الانتهاء

طبّق خطوات المراجعة في الملف `../fiper-landing-review/SKILL.md` (بالنسبة لمجلد هذه الـ skill) على الصفحة، ثم أخبر المستخدم:
- ما الذي أضفته أو غيّرته.
- أي `[placeholder]` أو `TODO` يحتاج منه محتوى حقيقياً.
