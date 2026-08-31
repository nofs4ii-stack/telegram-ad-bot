"use client";

import { useMemo, useState } from "react";
import { AdCard, Ad } from "./AdCard";

export const AdsList: React.FC<{
  initialAds: Ad[];
}> = ({ initialAds }) => {
  const [filter, setFilter] = useState<string>("all");

  const filtered = useMemo(() => {
    if (filter === "all") return initialAds;
    return initialAds.filter((ad) => (ad.status || "pending") === filter);
  }, [initialAds, filter]);

  return (
    <div className="space-y-8">
      <div className="flex flex-wrap gap-3 items-center justify-between">
        <div className="flex-1 min-w-[200px] flex items-center gap-4">
          <h2 className="text-2xl font-bold text-gray-900">
            الإعلانات
            <span className="ml-2 text-sm font-medium text-indigo-600">
              ({filtered.length})
            </span>
          </h2>
          <a
            href="/post"
            className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-br from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 shadow-lg transition-all duration-300 rounded-xl"
          >
            <span>نشر إعلان جديد</span>
          </a>
        </div>

        <div className="relative">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-3 text-sm rounded-xl border-2 border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 shadow-sm"
          >
            <option value="all">جميع الحالات</option>
            <option value="approved">موافق عليه فقط</option>
            <option value="pending">قيد المراجعة</option>
            <option value="rejected">مرفوض</option>
          </select>
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-2xl border border-gray-200 shadow-sm">
          <p className="text-2xl text-gray-400 mb-4">لا توجد إعلانات لعرضها</p>
          <a href="/post" className="inline-flex items-center gap-2 text-indigo-600 font-medium hover:underline">
            حاول نشر إعلان جديد
          </a>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filtered.map((ad: Ad) => (
            <AdCard key={ad.id} ad={ad} showActions={false} />
          ))}
        </div>
      )}
    </div>
  );
};