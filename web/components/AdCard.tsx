import React from 'react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { Tag } from 'lucide-react';
import Image from 'next/image';

export interface Ad {
  id: string;
  title: string;
  description: string;
  price?: number;
  category?: string;
  image_url?: string;
  status?: 'pending' | 'approved' | 'rejected';
  created_at?: string;
  user_id?: string;
}

const statusColors = {
  approved: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  pending: 'bg-amber-100 text-amber-800 border-amber-200',
  rejected: 'bg-red-100 text-red-800 border-red-200',
};

export const AdCard: React.FC<{
  ad: Ad;
  showActions?: boolean;
  onEdit?: (ad: Ad) => void;
  onDelete?: (ad: Ad) => void;
}> = ({ ad, showActions = false, onEdit, onDelete }) => {
  const status = ad.status || 'pending';

  return (
    <Card variant="elevated" className="group">
      <div className="aspect-video relative mb-4 overflow-hidden rounded-lg bg-gray-100">
        {ad.image_url ? (
          <Image
            src={ad.image_url}
            alt={ad.title}
            fill
            className="object-cover transition-transform group-hover:scale-105"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center text-gray-400">
            لا توجد صورة
          </div>
        )}
        <span
          className={`absolute top-3 left-3 px-2.5 py-1 text-xs font-semibold rounded-full border ${statusColors[status]}`}
        >
          {status === 'approved' && 'موافق عليه'}
          {status === 'pending' && 'قيد المراجعة'}
          {status === 'rejected' && 'مرفوض'}
        </span>
      </div>

      <div className="space-y-3">
        <div className="flex items-start justify-between gap-3">
          <h3 className="text-xl font-bold text-gray-900 flex-1">{ad.title}</h3>
          {ad.price && (
            <span className="whitespace-nowrap text-2xl font-bold text-indigo-700">
              {ad.price.toLocaleString('ar-EG')} جنيه
            </span>
          )}
        </div>

        <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">
          {ad.description || 'بدون وصف'}
        </p>

        {ad.category && (
          <div className="flex items-center gap-2">
            <Tag className="w-4 h-4 text-indigo-600" />
            <span className="px-2.5 py-1 text-xs font-medium bg-indigo-50 text-indigo-700 rounded-lg">
              {ad.category}
            </span>
          </div>
        )}

        {showActions && (
          <div className="flex gap-2 pt-2 opacity-100 md:group-hover:opacity-100 transition-opacity">
            <Button
              variant="outline"
              size="sm"
              className="flex-1"
              onClick={() => onEdit?.(ad)}
            >
              تعديل
            </Button>
            <Button
              variant="secondary"
              size="sm"
              className="flex-1 hover:bg-red-50 hover:text-red-700"
              onClick={() => onDelete?.(ad)}
            >
              حذف
            </Button>
          </div>
        )}
      </div>
    </Card>
  );
};