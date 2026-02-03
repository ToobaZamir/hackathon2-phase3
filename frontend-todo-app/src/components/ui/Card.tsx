import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  children: React.ReactNode;
}

const Card: React.FC<CardProps> = ({ title, children, className = '', ...props }) => {
  return (
    <div
      className={`bg-white shadow rounded-lg overflow-hidden ${className}`}
      {...props}
    >
      {title && (
        <div className="px-4 py-5 border-b border-gray-200 sm:px-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">{title}</h3>
        </div>
      )}
      <div className="px-4 py-5 sm:p-6">
        {children}
      </div>
    </div>
  );
};

export default Card;