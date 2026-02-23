import React from 'react';
import { useTranslation } from 'react-i18next';
import { Activity } from 'lucide-react';

const Header = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <header className="flex justify-between items-center p-6 border-b border-gray-800 bg-gray-900/50 backdrop-blur-md">
      <div className="flex items-center space-x-3">
        <Activity className="text-blue-500 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400">
            {t('title')}
          </h1>
          <p className="text-sm text-gray-400 font-medium">{t('subtitle')}</p>
        </div>
      </div>
      <div>
        <select 
          onChange={(e) => changeLanguage(e.target.value)} 
          value={i18n.resolvedLanguage}
          className="bg-gray-800 text-gray-300 px-3 py-1.5 rounded-lg border border-gray-700 outline-none focus:ring-2 focus:ring-blue-500 transition cursor-pointer"
        >
          <option value="en">EN</option>
          <option value="es">ES</option>
          <option value="pt">PT</option>
          <option value="fr">FR</option>
          <option value="de">DE</option>
        </select>
      </div>
    </header>
  );
};

export default Header;
