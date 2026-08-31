import { useState } from "react";

export const FilterBar: React.FC<{
  filter: string;
  onFilterChange: (value: string) => void;
}> = ({ filter, onFilterChange }) => {
  const options = [
    { value: "all", label: "جميع الحالات" },
    { value: "approved", label: "موافق عليه فقط" },
    { value: "pending", label: "قيد المراجعة" },
    { value: "rejected", label: "مرفوض" },
  ];

  return (
    <div className="flex flex-wrap gap-3 items-center">
      <div className="flex-1 min-w-0">
        <h2 className="text-2xl font-bold text-gray-900">
          السوق
          <span className="ml-2 text-sm font-medium text-indigo-600">
            للإعلانات
          </span>
        </h2>
      </div>

      <div className="relative w-[200px]">
        <select
          value={filter}
          onChange={(e) => onFilterChange(e.target.value)}
          className="w-full px-4 py-3 text-sm rounded-xl border-2 border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 shadow-sm"
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <a
        href="/post"
        className="flex items-center gap-2 px-5 py-3 text-sm font-semibold text-white bg-gradient-to-br from-indigo-600 to-violet-600 hover:from-indigo-500 hover:to-violet-500 shadow-lg hover:shadow-xl transition-all duration-300 rounded-xl"
      >
        <span className="w-4 h-4">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </span>
        <span>نشر إعلان جديد</span>
      </a>
    </div>
  );
};