'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';
import AdsList from '@/components/AdsList';

export default function HomePage() {
  const [ads, setAds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchAds() {
      const { data, error } = await supabase
        .from('ads')
        .select('*')
        .eq('status', 'approved');

      if (error) {
        console.error('Error fetching ads:', error);
      } else {
        console.log('Fetched ads:', data);
        setAds(data || []);
      }
      console.log('Supabase response:', { data, error });
      setLoading(false);
    }

    fetchAds();
  }, []);

  return (
    <main className="min-h-screen p-4 bg-gray-50">
      <h1 className="text-2xl font-bold mb-4 text-center">الإعلانات المقبولة</h1>
      {loading ? (
        <p className="text-center">جاري تحميل الإعلانات...</p>
      ) : (
        <AdsList ads={ads} />
      )}
    </main>
  );
}
