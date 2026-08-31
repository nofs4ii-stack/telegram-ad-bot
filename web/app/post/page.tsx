import type { Metadata } from "next";
import { AdForm } from "@/components/AdForm";
import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { supabase } from "@/lib/supabase";

export const metadata: Metadata = {
  title: "نشر إعلان جديد",
  description: "أنشئ إعلانك الآن وتواصل مع جمهور واسع",
};

export default function PostPage() {
  async function handleSubmit(data: any) {
    "use server";
    const { error } = await supabase
      .from("ads")
      .insert({
        title: data.title,
        description: data.description,
        price: data.price,
        category: data.category,
        image_url: data.image_url || null,
        status: "pending",
        user_id: data.user_id,
      })
      .select();
    if (error) throw new Error(error.message);
  }

  return (
    <main className="min-h-[90vh] bg-gradient-to-b from-indigo-50 via-white to-white">
      {/* Decorative top bar */}
      <div className="h-2 bg-gradient-to-r from-indigo-500 via-violet-500 to-amber-400" />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12 sm:py-16 space-y-8">
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="inline-flex items-center gap-2 px-3 py-1.5 text-sm font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors"
          >
            <ArrowRight className="w-4 h-4 rotate-180" />
            العودة للصفحة الرئيسية
          </Link>
        </div>

        <header className="text-center space-y-3">
          <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 tracking-tight">
            نشر <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-700">إعلان جديد</span>
          </h1>
          <p className="text-xl text-gray-500 max-w-xl mx-auto leading-relaxed">
            املأ البيانات أدناه لنشر إعلانك في السوق. بعد المراجعة سيتم عرض إعلانك للجمهور.
          </p>
        </header>

        <section className="bg-white rounded-2xl shadow-xl shadow-indigo-100/50 border border-gray-100 p-8 sm:p-10">
          <AdForm onSubmit={handleSubmit} />
        </section>
      </div>
    </main>
  );
}
