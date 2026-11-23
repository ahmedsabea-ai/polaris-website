#!/usr/bin/env python3
"""Builds /articles/ (index + one page per article) and sitemap.xml. Run: python3 build_articles.py"""
import html, json, os, re

SITE = "https://polarishd.co"
DATE = "2026-11-23"

PROG = {
    "lss": ("Lean Six Sigma Green Belt", "/#programmes", "برنامج Lean Six Sigma Green Belt من Polaris: سبعة أيام (56 ساعة) مع التحضير لامتحان IASSC."),
    "sc": ("Supply Chain", "/#programmes", "برنامج Supply Chain من Polaris: أربعون ساعة مع التحضير لامتحان CSCP من ASCM (APICS)."),
    "sim": ("Challenge of Egypt", "/#simulation", "Challenge of Egypt: محاكاة ليوم واحد (8 ساعات) من تصميم GamingWorks، يبني فيها الفريق هرمًا كمشروع كامل."),
}
TOPIC = {"lss": "Lean Six Sigma", "sc": "سلاسل الإمداد", "sim": "التعلم بالمحاكاة"}

ARTICLES = [
dict(slug="six-sigma-terms", prog="lss",
 title="أربعة مصطلحات في Six Sigma يجب أن تعرفها",
 desc="DPMO ومستوى سيجما وCTQ وقدرة العملية: أربعة مصطلحات تتكرر في أي مشروع Six Sigma، بشرح بسيط ومثال لكل واحد.",
 body="""
من يدخل عالم Six Sigma لأول مرة يصطدم بالاختصارات قبل أن يصل إلى الفكرة. الخبر الجيد أن أغلب النقاش يدور حول عدد قليل من المصطلحات، وإذا فهمت هذه الأربعة ستتابع أي اجتماع تحسين بسهولة.

## 1. DPMO: العيوب لكل مليون فرصة
هو المقياس الأساسي في Six Sigma. لا يسأل «كم منتجًا معيبًا خرج؟» بل «كم مرة أخطأنا من بين كل الفرص التي كان يمكن أن نخطئ فيها؟».
مثال: فاتورة فيها خمسة حقول يمكن أن يقع الخطأ في أي منها. إذا راجعت 1,000 فاتورة ووجدت 25 خطأ، فعدد الفرص 5,000 والنتيجة 5,000 عيب لكل مليون فرصة.

## 2. مستوى سيجما (Sigma level)
رقم واحد يلخص أداء العملية: كلما ارتفع قلّت العيوب. المستوى السادس، الذي أخذت المنهجية اسمها منه، يعني 3.4 عيب فقط لكل مليون فرصة. أغلب العمليات غير المحسّنة تقف عند المستوى الثالث أو الرابع، أي آلاف العيوب لكل مليون.

## 3. CTQ: الخصائص الحرجة للجودة
العميل لا يقول «أريد انحرافًا معياريًا أقل»، بل يقول «أريد طلبي في موعده». CTQ هي ترجمة صوت العميل إلى شيء يمكن قياسه: التسليم خلال 48 ساعة، أو نسبة خطأ في الفاتورة أقل من 1%. بدونها يتحسن ما لا يهم العميل.

## 4. قدرة العملية (Cp و Cpk)
تقارن بين ما يسمح به العميل (حدود المواصفة) وما تنتجه العملية فعلًا (تشتتها الطبيعي). Cp يقيس اتساع التشتت فقط، و Cpk يضيف سؤالًا ثانيًا: هل العملية متمركزة في المنتصف؟ القيمة 1.33 أو أكثر تعد في العادة علامة على عملية قادرة.

## كيف ترتبط الأربعة معًا؟
تبدأ من CTQ لتعرف ما يهم العميل، تقيس الوضع الحالي بـ DPMO، تعبّر عنه بمستوى سيجما، ثم تستخدم Cp و Cpk لتعرف هل المشكلة في التشتت أم في التمركز. هذا هو المسار الذي يتدرب عليه حامل الـ Green Belt في مرحلتي Measure و Analyze.
"""),
dict(slug="six-sigma-facts", prog="lss",
 title="خمس معلومات عن Six Sigma قد تسمعها لأول مرة",
 desc="من أين جاءت Six Sigma، ولماذا الرقم 3.4، وما علاقة الأحزمة بالفنون القتالية؟ خمس حقائق قصيرة عن المنهجية.",
 body="""
Six Sigma اسم يتردد كثيرًا في إعلانات الوظائف والدورات، لكن قصتها نفسها أقل شهرة. هذه خمس معلومات تساعدك على فهم المنهجية وليس فقط حفظ اسمها.

## 1. بدأت في مصنع إلكترونيات
ظهرت المنهجية في شركة Motorola في منتصف الثمانينيات على يد المهندس Bill Smith، ثم انتشرت عالميًا بعد أن اعتمدتها General Electric في التسعينيات وجعلتها جزءًا من طريقة إدارة الشركة كلها.

## 2. الرقم 3.4 ليس عشوائيًا
الهدف المعروف هو 3.4 عيب لكل مليون فرصة. هذا الرقم يفترض أن أي عملية تنحرف قليلًا مع الوقت عن مركزها، فتُحسب النتيجة مع هامش أمان لهذا الانحراف. أي أنه هدف واقعي لعملية تعمل لسنوات، وليس لحظة مثالية في المعمل.

## 3. الأحزمة مأخوذة من الفنون القتالية
Yellow Belt و Green Belt و Black Belt ليست درجات علمية، بل أدوار داخل المشروع. حامل الـ Green Belt يقود مشروع تحسين في مجال عمله بجانب وظيفته، وحامل الـ Black Belt يتفرغ عادة لمشاريع أكبر ويدعم الآخرين.

## 4. ليست للمصانع فقط
أي عمل يتكرر يمكن قياسه وتحسينه: زمن فتح حساب في بنك، أخطاء صرف الدواء في مستشفى، دقة تجهيز الطلبات في مخزن، أو زمن الرد على العميل في مركز اتصال.

## 5. Lean و Six Sigma يكملان بعضهما
Lean يسأل: أين نضيّع الوقت والمجهود؟ و Six Sigma يسأل: لماذا تختلف النتيجة من مرة لأخرى؟ الجمع بينهما في Lean Six Sigma يعطي عملية أسرع وأدق في الوقت نفسه، وهذا سبب أن أغلب البرامج اليوم تدرّس الاثنين معًا.
"""),
dict(slug="lean-six-sigma-competitive-edge", prog="lss",
 title="كيف تخسر شركتك مكانها في السوق بدون Lean Six Sigma؟",
 desc="خمس طرق تخسر بها الشركات المال والعملاء دون أن تلاحظ، وكيف يعالجها Lean Six Sigma بالقياس لا بالانطباع.",
 body="""
الشركات لا تخسر مكانها في السوق بقرار واحد خاطئ في الغالب، بل بتسرّب صغير يتكرر كل يوم. Lean Six Sigma موجود ليجعل هذا التسرّب مرئيًا ثم يوقفه. هذه أشهر صوره.

## 1. تكلفة الجودة الرديئة لا تظهر في أي تقرير
إعادة الشغل، المرتجعات، الخصومات التعويضية، وساعات الموظفين في تصحيح الأخطاء: كلها تكاليف حقيقية لكنها موزعة على بنود كثيرة فلا يراها أحد مجتمعة.

## 2. الهدر يصبح «طريقة العمل»
Lean يحدد ثمانية أنواع من الهدر: العيوب، الإنتاج الزائد، الانتظار، المواهب غير المستغلة، النقل، المخزون الزائد، الحركة الزائدة، والمعالجة الزائدة. حين تعتاد عليها المؤسسة تتوقف عن رؤيتها.

## 3. القرارات تُبنى على الانطباع
«أظن أن المشكلة في المورد» جملة تكلف كثيرًا. منهجية DMAIC تفرض ترتيبًا واضحًا: عرّف المشكلة، قِس، حلّل السبب الجذري، ثم حسّن. فلا يُصرف مال على حل قبل التأكد من السبب.

## 4. المشكلة نفسها تعود كل ربع سنة
كثير من التحسينات ينجح أسابيع ثم يختفي. المرحلة الأخيرة في DMAIC، وهي Control، وظيفتها تثبيت النتيجة بمؤشرات ومسؤوليات واضحة حتى لا تعود العملية إلى ما كانت عليه.

## 5. المنافس يتعلم أسرع
حين يملك المنافس فريقًا يعرف كيف يحوّل شكوى عميل إلى مشروع تحسين له بداية ونهاية، فهو يخفض تكلفته ويرفع جودته في كل دورة، والفجوة تتسع مع الوقت.

## من أين تبدأ؟
لا تحتاج إلى برنامج ضخم. ابدأ بعملية واحدة تؤلم العميل أو تكلف كثيرًا، وشخص مدرَّب على مستوى Green Belt يقود مشروعًا واحدًا عليها. نتيجة مشروع واحد ناجح أقوى من أي عرض تقديمي في إقناع الإدارة.
"""),
dict(slug="supply-chain-crisis-management", prog="sc",
 title="كيف يتعامل مدير سلاسل الإمداد مع الأزمات المفاجئة؟",
 desc="ست خطوات عملية لمدير سلسلة الإمداد قبل الأزمة وأثناءها وبعدها: من خريطة المخاطر إلى مراجعة الدروس.",
 body="""
تأخر شحنة، توقف مورد رئيسي، ارتفاع مفاجئ في الطلب، أو قرار جمركي جديد: الأزمة في سلسلة الإمداد مسألة وقت. الفرق بين شركة تتعثر وأخرى تكمل العمل هو ما تم تجهيزه قبلها.

## قبل الأزمة
### 1. ارسم خريطة المخاطر
حدّد المواد والموردين والمسارات التي يتوقف عليها العمل، وقيّم كل واحد بسؤالين: ما احتمال تعطله؟ وما أثر ذلك؟ ركّز على ما يجمع الاحتمال والأثر معًا.

### 2. لا تعتمد على مصدر واحد
للمواد الحرجة، جهّز موردًا بديلًا معتمدًا ومجرَّبًا ولو بكميات صغيرة. تكلفة المورد الثاني أقل كثيرًا من تكلفة خط متوقف.

### 3. ضع مخزون الأمان في مكانه الصحيح
ليس المطلوب زيادة المخزون في كل شيء، بل في الأصناف التي تجمع بين أهمية عالية ومدة توريد طويلة أو غير مستقرة.

## أثناء الأزمة
### 4. اجمع الصورة الكاملة بسرعة
ما المخزون المتاح؟ ما الطلبات المفتوحة؟ ما الشحنات في الطريق؟ قرار يُتخذ ببيانات ناقصة قد يخلق أزمة ثانية.

### 5. فريق واحد وقناة تواصل واحدة
المشتريات والتخطيط والمبيعات والمالية في غرفة واحدة، ورسالة واحدة واضحة للعملاء والموردين. العميل يتقبل التأخير المعلن أكثر من الصمت.

## بعد الأزمة
### 6. راجع وسجّل
ما الذي نجح؟ ما الذي تأخر؟ ما الذي نغيّره في الخطة؟ الأزمة التي لا تُراجَع تتكرر بنفس تكلفتها.

هذه الموضوعات، من إدارة المخاطر إلى تخطيط المخزون والعلاقة مع الموردين، جزء أساسي من محتوى شهادة CSCP.
"""),
dict(slug="supply-chain-trends", prog="sc",
 title="ما الذي يتغير في سلاسل الإمداد؟ خمسة اتجاهات تستحق المتابعة",
 desc="المرونة قبل التكلفة، الرؤية اللحظية، التوريد القريب، الاستدامة، ومهارات التحليل: خمسة اتجاهات تعيد تشكيل سلاسل الإمداد.",
 body="""
لسنوات طويلة كان السؤال الأول في سلاسل الإمداد: كيف نخفض التكلفة؟ الاضطرابات المتتالية في السنوات الأخيرة أضافت أسئلة أخرى بالأهمية نفسها. هذه خمسة اتجاهات تظهر في أغلب الشركات مهما كان حجمها.

## 1. المرونة قبل أقل تكلفة
سلسلة مصممة لأقل تكلفة فقط تنكسر عند أول صدمة. الشركات تقبل اليوم تكلفة أعلى قليلًا مقابل بدائل جاهزة: مورد ثانٍ، مسار شحن بديل، أو مخزون أمان مدروس.

## 2. الرؤية اللحظية
معرفة مكان الشحنة وحالة المخزون وطلبات العملاء في الوقت نفسه لم تعد رفاهية. الجداول المتفرقة تُستبدل بأنظمة تربط التخطيط بالمشتريات والمخازن.

## 3. التوريد القريب
تقصير المسافة بين المورد والمصنع والعميل يقلل مدة التوريد ومخاطر الشحن الطويل. ليس مناسبًا لكل صنف، لكنه صار خيارًا يُدرس بجدية مع كل تعاقد جديد.

## 4. الاستدامة أصبحت مطلبًا
العملاء والجهات التنظيمية يسألون عن مصدر المواد وأثر النقل والتعبئة. مدير سلسلة الإمداد مطلوب منه أرقام عن هذا، وليس مجرد نوايا.

## 5. التحليل مهارة أساسية
التنبؤ بالطلب، تحديد مستويات المخزون، وتقييم الموردين كلها قرارات تعتمد على البيانات. المتخصص الذي يجمع فهم العمليات مع قراءة الأرقام هو الأكثر طلبًا.

## ماذا يعني ذلك لك؟
إذا كنت تعمل في المشتريات أو التخطيط أو المخازن، فالنظرة الشاملة للسلسلة من المورد إلى العميل هي ما يميزك. وهذه بالضبط زاوية شهادة CSCP: السلسلة كلها، وليس وظيفة واحدة داخلها.
"""),
dict(slug="global-logistics-challenges", prog="sc",
 title="ستة تحديات لوجستية تواجهك عند دخول السوق العالمي",
 desc="الجمارك، Incoterms، مدد الشحن، التكلفة الكلية للوصول، العملة، والمرتجعات: ما يجب تجهيزه قبل أول شحنة تصدير أو استيراد.",
 body="""
البيع أو الشراء خارج بلدك يفتح سوقًا أكبر، لكنه يضيف طبقات لا تظهر في التجارة المحلية. معرفة هذه التحديات مبكرًا أرخص كثيرًا من اكتشافها مع أول شحنة محتجزة.

## 1. الجمارك والمستندات
كل بلد له قواعده في التصنيف الجمركي وشهادات المنشأ والمطابقة. خطأ في بند واحد قد يوقف الشحنة أيامًا. الحل: مخلّص جمركي موثوق، وقائمة مستندات ثابتة لكل وجهة.

## 2. من يتحمل ماذا؟ (Incoterms)
شروط مثل EXW و FOB و CIF و DAP و DDP تحدد أين تنتقل المسؤولية والتكلفة والمخاطر من البائع إلى المشتري. اختيار الشرط الخطأ قد يحمّلك شحنًا وتأمينًا لم تحسبهما في السعر.

## 3. مدد الشحن وتذبذبها
المشكلة ليست فقط أن الشحن الدولي أطول، بل أنه أقل انتظامًا. خطّط على المدة المتوقعة مع هامش، واحسب مخزون الأمان على أساس التذبذب لا المتوسط.

## 4. التكلفة الكلية للوصول (Landed cost)
سعر المنتج عند المورد جزء من القصة. أضف الشحن والتأمين والرسوم الجمركية والتخليص والنقل الداخلي والتخزين. المقارنة بين الموردين تكون على التكلفة عند باب مخزنك.

## 5. العملة وشروط الدفع
تغيّر سعر الصرف بين يوم الطلب ويوم السداد قد يمحو هامش الربح. اتفق على العملة وطريقة الدفع وتوقيته بوضوح، وراجع أثر ذلك على التدفق النقدي.

## 6. التوصيل الأخير والمرتجعات
تسليم العميل النهائي في بلد آخر وإرجاع منتج منه أعقد وأغلى مما تتوقع. حدّد سياسة المرتجعات وشريك التوصيل المحلي قبل أن تبدأ البيع، لا بعد أول شكوى.

## الخلاصة
اللوجستيات الدولية ليست وظيفة قسم الشحن وحده، بل قرار يشترك فيه المشتريات والمالية والمبيعات. وفهم الصورة الكاملة هو ما تبنيه دراسة سلاسل الإمداد بشكل منهجي.
"""),
dict(slug="inventory-management-tools", prog="sc",
 title="فئات الأدوات المستخدمة في إدارة المخزون",
 desc="خمس فئات من أدوات إدارة المخزون: التصنيف، تحديد الكميات، التخطيط، دقة السجلات، ومؤشرات الأداء، مع أشهر أداة في كل فئة.",
 body="""
إدارة المخزون توازن دائم بين خطرين: نفاد الصنف وخسارة البيع، أو تكدسه وتجميد المال. الأدوات كثيرة، لكن يمكن ترتيبها في خمس فئات، كل واحدة تجيب عن سؤال مختلف.

## 1. أدوات التصنيف: أين أركّز؟
- تحليل ABC: يرتب الأصناف حسب قيمتها. نسبة صغيرة من الأصناف (A) تمثل في العادة أغلب قيمة المخزون وتستحق أدق متابعة.
- تحليل XYZ: يرتبها حسب انتظام الطلب. X طلب مستقر، و Z طلب متقلب يصعب التنبؤ به.
الجمع بينهما يحدد سياسة مختلفة لكل مجموعة بدل قاعدة واحدة للجميع.

## 2. أدوات تحديد الكمية والتوقيت: كم أطلب ومتى؟
- الكمية الاقتصادية للطلب (EOQ): توازن بين تكلفة إصدار الطلب وتكلفة الاحتفاظ بالمخزون.
- نقطة إعادة الطلب (ROP): الاستهلاك المتوقع خلال مدة التوريد مضافًا إليه مخزون الأمان.
- مخزون الأمان (Safety stock): يغطي تذبذب الطلب وتأخر المورد.

## 3. أدوات التخطيط: ماذا سأحتاج لاحقًا؟
- MRP: يحسب احتياجات المواد الخام من خطة الإنتاج وقوائم المواد.
- DRP: يوزع المخزون على الفروع والمخازن حسب الطلب المتوقع في كل موقع.

## 4. أدوات دقة السجلات: هل الرقم في النظام صحيح؟
- الجرد الدوري (Cycle counting): عدّ جزء من الأصناف كل يوم بدل إيقاف العمل لجرد سنوي شامل.
- الباركود وتتبع المواقع: يقللان أخطاء الإدخال والصرف.

## 5. مؤشرات الأداء: هل أدير المخزون جيدًا؟
- معدل دوران المخزون (Inventory turnover).
- أيام التغطية (Days of supply).
- نسبة تلبية الطلب (Fill rate).

## كيف تختار؟
ابدأ بالتصنيف، لأنه يحدد أين يستحق المجهود. ثم طبّق أدوات الكمية والتوقيت على أصناف A أولًا، وتابع النتيجة بمؤشرين أو ثلاثة فقط. هذه الأدوات كلها تُدرّس ضمن تخطيط المخزون في مناهج سلاسل الإمداد مثل CSCP.
"""),
dict(slug="why-gamification-works", prog="sim",
 title="لماذا يعد التعلم بالمحاكاة واللعب مناسبًا لتطوير المهارات؟",
 desc="خمسة أسباب تجعل المحاكاة والـ Gamification أقوى من المحاضرة في تعليم المهارات العملية، ومتى لا تكون الاختيار المناسب.",
 body="""
أغلبنا حضر دورة ممتازة ثم عاد إلى مكتبه ولم يتغير شيء في طريقة عمله. المشكلة في الغالب ليست في المحتوى، بل في أن المهارة لا تُكتسب بالاستماع. هنا يأتي دور المحاكاة والـ Gamification.

## ما الفرق بين المصطلحين؟
الـ Gamification هو استخدام عناصر اللعب، مثل النقاط والأدوار والتحديات، في سياق تعليمي. والمحاكاة (Business simulation) تذهب أبعد: فريق يدير موقفًا يشبه الواقع ويتخذ قرارات لها نتائج. الاثنان يقومان على فكرة واحدة: التعلم بالتجربة.

## 1. تمارس بدل أن تسمع
حين تتخذ قرارًا بنفسك وترى نتيجته، ترتبط المعلومة بتجربة وليس بشريحة عرض. وهذا ما يبقى في الذاكرة بعد شهور.

## 2. النتيجة تظهر فورًا
في العمل الحقيقي قد تنتظر شهورًا لتعرف أثر قرارك. في المحاكاة ترى الأثر خلال دقائق، فتجرّب وتصحح أكثر من مرة في يوم واحد.

## 3. الخطأ آمن
مكان آمن للخطأ هو أفضل مكان للتعلم. فريق يفشل في الجولة الأولى ويفهم السبب يتعلم أكثر من فريق سمع قائمة نصائح.

## 4. الكل يشارك
لا يوجد مستمع في الصف الأخير. كل مشارك له دور، والفريق ينجح أو يتعثر معًا، فتظهر مهارات التواصل وتوزيع الأدوار كما هي في الواقع.

## 5. الربط بالعمل يحدث في النقاش
أهم جزء ليس اللعب نفسه بل جلسة النقاش بعده: ماذا حدث؟ لماذا؟ وأين نرى الشيء نفسه في شركتنا؟ هنا تتحول التجربة إلى خطوات تُطبق.

## متى لا تكون مناسبة؟
إذا كان الهدف حفظ معلومات أو اجتياز امتحان نظري، فالدراسة المنظمة أسرع. المحاكاة أقوى حين يكون الهدف تغيير سلوك: التخطيط، العمل كفريق، التواصل، واتخاذ القرار تحت ضغط.
"""),
dict(slug="choosing-simulation-training", prog="sim",
 title="خمسة أسئلة قبل أن تختار دورة تدريبية بالمحاكاة",
 desc="ليست كل دورة فيها لعبة تدريبًا بالمحاكاة. خمسة أسئلة تساعدك على اختيار برنامج يغيّر طريقة عمل فريقك فعلًا.",
 body="""
انتشرت الدورات التي تعلن أنها «تفاعلية» أو «بالألعاب»، لكن الفرق كبير بين نشاط ممتع في منتصف اليوم ومحاكاة مصممة لتغيير طريقة عمل الفريق. هذه خمسة أسئلة تكشف الفرق قبل أن تدفع.

## 1. هل اللعبة مرتبطة بأهداف تعلّم محددة؟
اسأل: ماذا سيفعل فريقي بشكل مختلف بعد هذا اليوم؟ المحاكاة الجيدة تُبنى حول مهارات واضحة، مثل التخطيط وإدارة المخاطر وتوزيع الأدوار، وليست فقرة ترفيهية.

## 2. من صمّم المحاكاة؟
المحاكاة التي طوّرتها جهة متخصصة وجُرّبت مع مئات الفرق تختلف عن لعبة ارتجلها المدرب. اسأل عن المصدر، وعن اعتماد المدرب لتقديمها.

## 3. هل هناك جولات متعددة؟
التعلم يحدث حين يجرّب الفريق، يرى النتيجة، يعدّل طريقته، ثم يجرّب مرة أخرى. جولة واحدة لا تكفي لرؤية أثر التغيير.

## 4. كم وقت النقاش بعد كل جولة؟
جلسة النقاش (Debrief) هي ما يحوّل اللعب إلى تعلّم. إذا كان البرنامج لعبًا متواصلًا بلا توقف للتحليل، فالفائدة ستبقى داخل القاعة.

## 5. هل تخرج بخطة للتطبيق؟
اليوم الناجح ينتهي بقائمة قصيرة: ما الذي سنبدأه، وما الذي سنوقفه، ومن المسؤول. بدونها يعود كل شيء كما كان يوم الأحد.

## مثال: Challenge of Egypt
في هذه المحاكاة من تصميم GamingWorks يعمل المشاركون كفريق مشروع مكلف ببناء هرم: يخططون، يوزعون الأدوار، يتعاملون مع المخاطر والتغييرات، ثم يتوقفون بعد كل مرحلة ليحللوا ما حدث ويحسّنوا طريقتهم. هي مناسبة للفرق التي تعمل معًا على مشاريع وتريد لغة مشتركة في التخطيط والتنفيذ.
"""),
]

CSS = """
:root{--night:#0B2038;--nile:#2A6CA6;--gold:#D6A94A;--stone:#E8ECF1;--ink:#14202E;--muted:#55636F;--paper:#fff;--wrap:1120px;
--body:"IBM Plex Sans Arabic","IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif}
*{box-sizing:border-box}
body{margin:0;font-family:var(--body);font-size:18px;line-height:1.9;color:var(--ink);background:var(--paper)}
img,svg{max-width:100%;display:block}
a{color:var(--nile)}
:focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:4px}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 24px}
.site-header{border-bottom:1px solid var(--stone);background:#fff;position:sticky;top:0;z-index:10}
.site-header .wrap{display:flex;align-items:center;gap:24px;min-height:68px}
.brand img{height:46px;width:auto}
.nav{display:flex;gap:22px;margin-inline-start:auto;flex-wrap:wrap}
.nav a{text-decoration:none;font-weight:500;font-size:.98rem;color:var(--ink)}
.nav a:hover,.nav a[aria-current]{color:var(--nile)}
.btn{display:inline-block;white-space:nowrap;text-decoration:none;font-weight:600;font-size:1rem;padding:.6em 1.2em;border-radius:6px;background:var(--night);color:#fff}
h1,h2,h3{line-height:1.45;margin:0;font-weight:700;color:var(--night)}
h1{font-size:clamp(1.8rem,4.2vw,2.7rem)}
.lead{background:var(--night);color:#fff;padding:56px 0 48px}
.lead h1{color:#fff;max-width:22em}
.lead p{color:#C9D5E2;max-width:40em;margin:.8em 0 0;font-size:1.08rem}
.crumb{font-size:.92rem;color:#9FB3C8;margin:0 0 1em}
.crumb a{color:#DCE6F0}
.topic{display:inline-block;color:var(--gold);font-weight:600;font-size:.98rem;margin-bottom:.5em}
article{max-width:44em;margin:0 auto;padding:44px 24px 20px}
article p{margin:0 0 1.15em}
article h2{font-size:1.45rem;margin:1.7em 0 .5em}
article h3{font-size:1.15rem;margin:1.3em 0 .3em;color:var(--nile)}
article ul{margin:0 0 1.2em;padding-inline-start:1.3em}
article li{margin-bottom:.45em}
.cta{max-width:44em;margin:10px auto 60px;padding:0 24px}
.cta div{border:1px solid var(--stone);border-inline-start:6px solid var(--gold);border-radius:8px;padding:24px 26px;background:#FAFBFC}
.cta p{margin:0 0 .9em}
.more{max-width:44em;margin:0 auto 70px;padding:0 24px}
.more h2{font-size:1.2rem;margin-bottom:.6em}
.more ul{list-style:none;margin:0;padding:0}
.more li{border-top:1px solid var(--stone);padding:.7em 0}
.more a{text-decoration:none;font-weight:500}
.group{padding:44px 0 6px}
.group h2{font-size:1.5rem;margin-bottom:.9em}
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.cards li{border:1px solid var(--stone);border-radius:8px;padding:22px 22px 18px}
.cards h3{font-size:1.14rem;margin-bottom:.45em}
.cards h3 a{color:var(--night);text-decoration:none}
.cards h3 a:hover{color:var(--nile)}
.cards p{margin:0;color:var(--muted);font-size:.98rem;line-height:1.75}
footer{border-top:1px solid var(--stone);padding:26px 0;margin-top:50px;font-size:.95rem;color:var(--muted)}
footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap}
footer a{color:inherit}
.en{direction:ltr;unicode-bidi:isolate}
@media (max-width:720px){.site-header .wrap{flex-wrap:wrap;padding-top:10px;padding-bottom:10px;gap:10px 18px}.nav{margin-inline-start:0;width:100%;order:3;gap:14px}.nav a{font-size:.9rem}.btn{margin-inline-start:auto}}
"""

HEAD = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Polaris Human Development</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/assets/favicon-192.png">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/articles/articles.css">
{jsonld}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Polaris Human Development، الصفحة الرئيسية"><img src="/assets/polaris-logo.png" alt="Polaris Human Development" width="1299" height="462"></a>
    <nav class="nav" aria-label="القائمة الرئيسية">
      <a href="/#programmes">البرامج</a>
      <a href="/#simulation"><span class="en">Challenge of Egypt</span></a>
      <a href="/articles/"{cur}>المقالات</a>
      <a href="/#contact">تواصل معنا</a>
    </nav>
    <a class="btn" href="https://wa.me/201028332844" rel="noopener">واتساب</a>
  </div>
</header>
<main>
"""
FOOT = """</main>
<footer>
  <div class="wrap">
    <span>© 2026 <span class="en">Polaris for Human Development</span></span>
    <span><a href="mailto:info@polarishd.co">info@polarishd.co</a> &nbsp; <a href="/">polarishd.co</a></span>
  </div>
</footer>
</body>
</html>
"""

LATIN = re.compile(r"[A-Za-z][A-Za-z0-9&.\-]*(?:[ /][A-Za-z0-9&.\-]+)*")
def esc(t):
    return html.escape(t, quote=False)
def render(body):
    out, in_ul = [], False
    for raw in body.strip().split("\n"):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append("<li>" + esc(line[2:]) + "</li>"); continue
        if in_ul:
            out.append("</ul>"); in_ul = False
        if line.startswith("### "):
            out.append("<h3>" + esc(line[4:]) + "</h3>")
        elif line.startswith("## "):
            out.append("<h2>" + esc(line[3:]) + "</h2>")
        else:
            out.append("<p>" + esc(line) + "</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)

def page_head(title, desc, url, ogtype, jsonld="", cur=""):
    return HEAD.format(title=html.escape(title), desc=html.escape(desc), url=url, ogtype=ogtype, site=SITE, jsonld=jsonld, cur=cur)

os.makedirs("articles", exist_ok=True)
open("articles/articles.css", "w", encoding="utf-8").write(CSS.strip() + "\n")
urls = [SITE + "/", SITE + "/articles/"]
for a in ARTICLES:
    url = f"{SITE}/articles/{a['slug']}/"
    urls.append(url)
    pname, plink, ptext = PROG[a["prog"]]
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "inLanguage": "ar",
          "datePublished": DATE, "dateModified": DATE, "mainEntityOfPage": url,
          "author": {"@type": "Organization", "name": "Polaris Human Development", "url": SITE},
          "publisher": {"@type": "Organization", "name": "Polaris Human Development", "logo": {"@type": "ImageObject", "url": SITE + "/assets/polaris-logo.png"}}}
    related = [b for b in ARTICLES if b["prog"] == a["prog"] and b is not a]
    h = page_head(a["title"], a["desc"], url, "article", '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    h += f"""<section class="lead"><div class="wrap">
  <p class="crumb"><a href="/">الرئيسية</a> / <a href="/articles/">المقالات</a></p>
  <span class="topic">{esc(TOPIC[a['prog']])}</span>
  <h1>{esc(a['title'])}</h1>
  <p>{esc(a['desc'])}</p>
</div></section>
<article>
{render(a['body'])}
</article>
<aside class="cta"><div>
  <p>{esc(ptext)}</p>
  <a class="btn" href="{plink}">تفاصيل البرنامج</a>
</div></aside>
<nav class="more" aria-label="مقالات ذات صلة">
  <h2>اقرأ أيضًا</h2>
  <ul>
""" + "\n".join(f'    <li><a href="/articles/{b["slug"]}/">{esc(b["title"])}</a></li>' for b in related) + """
  </ul>
</nav>
""" + FOOT
    os.makedirs(f"articles/{a['slug']}", exist_ok=True)
    open(f"articles/{a['slug']}/index.html", "w", encoding="utf-8").write(h)

idx = page_head("مقالات في سلاسل الإمداد و Lean Six Sigma والتعلم بالمحاكاة",
                "مقالات عملية قصيرة بالعربية من Polaris عن سلاسل الإمداد وإدارة المخزون و Lean Six Sigma والتدريب بالمحاكاة.",
                SITE + "/articles/", "website", cur=' aria-current="page"')
idx += """<section class="lead"><div class="wrap">
  <p class="crumb"><a href="/">الرئيسية</a></p>
  <h1>المقالات</h1>
  <p>شروحات عملية قصيرة في المجالات الثلاثة التي ندرّب عليها: سلاسل الإمداد، Lean Six Sigma، والتعلم بالمحاكاة.</p>
</div></section>
<div class="wrap">
"""
for key in ("lss", "sc", "sim"):
    idx += f'<section class="group"><h2>{esc(TOPIC[key])}</h2>\n<ul class="cards">\n'
    for a in ARTICLES:
        if a["prog"] == key:
            idx += f'  <li><h3><a href="/articles/{a["slug"]}/">{esc(a["title"])}</a></h3><p>{esc(a["desc"])}</p></li>\n'
    idx += "</ul></section>\n"
idx += "</div>\n" + FOOT
open("articles/index.html", "w", encoding="utf-8").write(idx)

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n" for u in urls) + "</urlset>\n"
open("sitemap.xml", "w", encoding="utf-8").write(sm)
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
print(len(ARTICLES), "articles,", len(urls), "urls")
