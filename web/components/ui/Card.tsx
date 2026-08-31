import React from 'react';

interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'elevated' | 'outlined';
}

export const Card: React.FC<CardProps> = ({
  title,
  children,
  className = '',
  variant = 'default',
}) => {
  const base = 'rounded-xl overflow-hidden shadow-sm transition-shadow hover:shadow-md';
  const variantStyles = {
    default: 'bg-white p-6',
    elevated: 'bg-white p-6 shadow-lg',
    outlined: 'border border-gray-200 bg-gray-50 p-6',
  };

  return (
    <div className={`${base} ${variantStyles[variant]} ${className}`}>
      {title && (
        <div className="flex items-center justify-between border-b border-gray-200 pb-3 mb-4">
          <h2 className="text-xl font-semibold">{title}</h2>
        </div>
      )}
      {children}
    </div>
  );
};