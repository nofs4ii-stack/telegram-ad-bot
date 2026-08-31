"use client";

import React, { useState } from 'react';
import { Button } from './ui/Button';
import { Input } from './ui/Input';
import { Textarea } from './ui/Textarea';
import { Select } from './ui/Select';
import { supabase } from '@/lib/supabase';

const CATEGORIES = [
  'عقارات',
  'سيارات',
  'إلكترونيات',
  'ملابس',
  'خدمات',
  'وظائف',
  'أخرى',
];

export const AdForm: React.FC<{
  onSubmit: (data: Omit<any, 'id' | 'created_at' | 'user_id'>) => Promise<void>;
}> = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    category: CATEGORIES[0],
    image_url: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) newErrors.title = 'العنوان مطلوب';
    if (!formData.description.trim()) newErrors.description = 'الوصف مطلوب';
    if (formData.price && (isNaN(Number(formData.price)) || Number(formData.price) <= 0)) {
      newErrors.price = 'السعر يجب أن يكون رقمًا موجبًا';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) return;
    setIsSubmitting(true);
    setSuccessMessage(null);

    try {
      const formDataNumber = {
        ...formData,
        price: formData.price ? Number(formData.price) : undefined,
      };

      // Determine user_id from auth (for now, using a mock user)
      const { data: { user } } = await supabase.auth.getUser();
      const userId = user?.id || 'mock-user-id';

      await onSubmit({
        ...formDataNumber,
        user_id: userId,
        status: 'pending', // New ads start as pending for review
      });

      setSuccessMessage('تم إرسال الإعلان بنجاح! تحت المراجعة.');
      setFormData({
        title: '',
        description: '',
        price: '',
        category: CATEGORIES[0],
        image_url: '',
      });
    } catch (error: any) {
      console.error('Error submitting ad:', error);
      setErrors({ submit: error.message || 'فشل الإرسال. يرجى المحاولة مرة أخرى.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900">إنشاء إعلان جديد</h2>
      <p className="text-gray-600 max-w-md">املأ البيانات لنشر إعلانك في السوق</p>

      {successMessage && (
        <div className="p-4 bg-emerald-50 border-l-4 border-emerald-400 text-emerald-700">
          {successMessage}
        </div>
      )}

      <div className="space-y-4">
        <Input
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="أدخل عنوان الإعلان"
          error={errors.title}
          label="العنوان"
          helperText="حد أقصى 100 حرف"
        />

        <Textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="صف الإعلان بالتفصيل"
          rows={4}
          error={errors.description}
          label="الوصف"
          helperText="وصف واضح ومفصل يجلب المزيد من المشاهدات"
        />

        <div className="grid grid-cols-2 gap-4">
          <Input
            name="price"
            type="number"
            value={formData.price}
            onChange={handleChange}
            placeholder="0.00"
            error={errors.price}
            label="السعر (اختياري)"
            helperText="بدون رموز أو فواصل"
          />

          <Select
            name="category"
            value={formData.category}
            onChange={handleChange}
            label="الفئة"
            className=""
          />
        </div>

        <Input
          name="image_url"
          value={formData.image_url}
          onChange={handleChange}
          placeholder="https://example.com/image.jpg"
          label="رابط الصورة (اختياري)"
          helperText="الرابط المباشر لصورة الإعلان (يبدأ بـ http أو https)"
        />
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <Button
          variant="secondary"
          size="lg"
          onClick={() => setFormData({
            title: '',
            description: '',
            price: '',
            category: CATEGORIES[0],
            image_url: '',
          })}
        >
          مسح النموذج
        </Button>
        <Button
          variant="primary"
          size="lg"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? 'جاري الإرسال...' : 'نشر الإعلان'}
        </Button>
      </div>
    </form>
  );
};