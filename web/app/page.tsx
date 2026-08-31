import type { Metadata } from "next";
import { supabase } from "@/lib/supabase";
import { AdsList } from "@/components/AdsList";

export const metadata: Metadata = {
  title: "السوق - الإعلانات",
  description: "تصفح أحدث الإعلانات في جميع الفئات",
};

export default async function HomePage() {
  // Debug: طباعة معلومات بدء جلب الإعلانات
  console.log("🔄 [DEBUG] بدء جلب الإعلانات من Supabase...");

  const { data: ads, error } = await supabase
    .from("ads")
    .select("*")
    .order("created_at", { ascending: false });

  // Debug: طباعة البيانات والخطأ
  console.log("📊 [DEBUG] البيانات المستلمة:", ads);
  console.log("❌ [DEBUG] الخطأ (إن وجد):", error);

  if (error) {
    console.error("💥 [DEBUG] حدث خطأ أثناء جلب الإعلانات:", error.message, error.details);
    return (
      <main className="min-h-[90vh] bg-gradient-to-b from-indigo-50 via-white to-white">
        <div className="h-2 bg-gradient-to-r from-indigo-500 via-violet-500 to-amber-400" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
          <div className="p-6 bg-red-50 border-l-4 border-red-400 text-red-800 rounded-lg">
            <p className="font-medium">خطأ في تحميل الإعلانات: {error.message}</p>
          </div>
        </div>
      </main>
    );
  }

  // Debug: طباعة عدد الإعلانات
  console.log(`✅ [DEBUG] تم جلب ${ads?.length || 0} إعلان بنجاح`);

  return (
    <main className="min-h-[90vh] bg-gradient-to-b from-indigo-50 via-white to-white">
      {/* Top decorative element */}
      <div className="h-2 bg-gradient-to-r from-indigo-500 via-violet-500 to-amber-400" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-10">
        <header className="text-center space-y-3 max-w-2xl mx-auto">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 tracking-tight">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-700">السوق</span>
            <span className="block text-2xl sm:text-3xl mt-2 text-gray-700">للإعلانات المعتمدة</span>
          </h1>
          <p className="text-lg text-gray-500 leading-relaxed">
            اكتشف أحدث الإعلانات في مختلف الفئات. كل إعلان يمر بمراجعة قبل عرضه.
          </p>
        </header>

        <AdsList initialAds={ads || []} />
      </div>
    </main>
  );
}