---
name: fiper-landing-review
disable-model-invocation: true
argument-hint: "[وصف ما تريد]"
description: مراجعة وفحص جودة صفحة هبوط فايبر قبل النشر — الجوال، RTL، الوصولية، SEO، الأداء، الالتزام بالهوية. Review/QA the Fiper landing page before shipping — mobile, RTL, accessibility, SEO, performance and brand compliance. Use after building or changing a section, or when asked to "check"/"review"/"راجع" the page.
---

# مراجعة صفحة هبوط فايبر

## طلب المستخدم

$ARGUMENTS

إذا لم يُذكر ملف، فابحث عن `index.html` في جذر المشروع.

## 1. الفحص الآلي

شغّل سكربت الفحص الموجود في مجلد `scripts/` داخل مجلد هذه الـ skill، من جذر المشروع وعلى ملف الصفحة:

```bash
python3 <مجلد هذه الـ skill>/scripts/check_landing.py index.html
```

يفحص السكربت: `lang`/`dir`، و`<title>` و`meta description` وطولهما، ووجود `h1` واحد، ووجود `alt` لكل صورة،
وأبعاد الصور، و`viewport`، وألوان مكتوبة مباشرة خارج `:root`، واستعمال `left`/`right` بدل الخصائص المنطقية،
ووجود `TODO` أو `[placeholder]` لم يُستبدل.
أصلح كل **ERROR** قبل النشر، وراجع كل **WARN**.

## 2. فحص بصري (إن توفر متصفح)

Playwright متاح في بيئات Claude Code السحابية. التقط صوراً للصفحة على ثلاثة عروض:

```bash
python3 - <<'EOF'
from playwright.sync_api import sync_playwright
import pathlib
page_url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (375, 768, 1280):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto(page_url)
        overflow = pg.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        print(f"{w}px horizontal overflow: {overflow}")
        pg.screenshot(path=f"/tmp/fiper-{w}.png", full_page=True)
    b.close()
EOF
```

اعرض الصور وتحقق من التالي: لا يوجد تمرير أفقي، والنص العربي يبدأ من اليمين، وزر CTA ظاهر قبل التمرير في Hero.

## 3. قائمة المراجعة اليدوية

**الهوية**
- [ ] الألوان من `var(--fiper-*)` فقط، والخطوط حسب الملف `../fiper-brand/SKILL.md` (بالنسبة لمجلد هذه الـ skill).
- [ ] اللون الأساسي مستخدم للإجراء الرئيسي فقط.

**المحتوى**
- [ ] `h1` واحد، وتسلسل العناوين بلا قفز (من h2 إلى h3).
- [ ] لا أرقام ولا شهادات مختلقة، ولا يوجد `[placeholder]` منسيّ.
- [ ] كل زر يحمل فعلاً واضحاً، وكل الروابط الداخلية `#id` تشير إلى أقسام موجودة.

**الوصولية**
- [ ] تباين الألوان 4.5:1 على الأقل.
- [ ] التنقل بلوحة المفاتيح يعمل و`:focus-visible` ظاهر.
- [ ] الأيقونات الزخرفية عليها `aria-hidden="true"`.

**الأداء**
- [ ] الصور بصيغة WebP أو AVIF، وكل صورة تحت Hero عليها `loading="lazy"`.
- [ ] الخطوط محمّلة بـ `display=swap`، وأي سكربتات خارجية غير ضرورية محذوفة.

**SEO والمشاركة**
- [ ] وسوم `og:title` و`og:description` و`og:image` و`twitter:card` موجودة.
- [ ] وسم `<link rel="canonical">` و`favicon` موجودان.

## 4. التقرير

قدّم للمستخدم تقريراً قصيراً فيه:
- ما نجح.
- ما أصلحته.
- ما يحتاج قراره أو محتواه، مثل الـ TODO والصور الحقيقية والأرقام.
