import React from 'react';
import { useTranslation } from 'react-i18next';
import { Settings, Zap, Compass, Ruler, FastForward } from 'lucide-react';

const ParamControls = ({ params, setParams }) => {
  const { t } = useTranslation();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setParams(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }));
  };

  const InputGroup = ({ icon: Icon, label, name, value, min, max, step = 1, colorCls }) => (
    <div className="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-gray-500 transition-colors">
      <div className="flex justify-between items-center mb-2">
        <label className="text-sm font-medium text-gray-300 flex items-center space-x-2">
          <Icon className={`w-4 h-4 ${colorCls}`} />
          <span>{label}</span>
        </label>
        <span className="text-sm font-bold bg-gray-900 px-2 py-1 rounded w-16 text-center shadow-inner">
          {value}
        </span>
      </div>
      <input
        type="range"
        name={name}
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleInputChange}
        className="w-full accent-blue-500 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
      />
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold flex items-center space-x-2 text-gray-200 mb-4 border-b border-gray-800 pb-2">
          <Settings className="w-5 h-5 text-gray-400" />
          <span>{t('settings')}</span>
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
          <InputGroup icon={Zap} label={t('cut_speed')} name="cut_speed" value={params.cut_speed} min="1" max="50" colorCls="text-red-500" />
          <InputGroup icon={Zap} label={t('mark_speed')} name="vector_engrave_speed" value={params.vector_engrave_speed} min="10" max="200" colorCls="text-green-500" />
          <InputGroup icon={Zap} label={t('raster_speed')} name="raster_engrave_speed" value={params.raster_engrave_speed} min="50" max="600" colorCls="text-blue-500" />
          <InputGroup icon={FastForward} label={t('transit_speed')} name="transit_speed" value={params.transit_speed} min="50" max="600" colorCls="text-purple-400" />
        </div>
      </div>

      <div>
         <h3 className="text-lg font-semibold flex items-center space-x-2 text-gray-200 mb-4 border-b border-gray-800 pb-2">
          <Compass className="w-5 h-5 text-gray-400" />
          <span>{t('advanced')}</span>
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <InputGroup icon={FastForward} label={t('acceleration')} name="accel" value={params.accel} min="50" max="2000" step="50" colorCls="text-orange-400" />
          <InputGroup icon={Ruler} label={t('ppi')} name="ppi" value={params.ppi} min="10" max="300" step="0.1" colorCls="text-teal-400" />
          <InputGroup icon={Ruler} label={t('scan_gap')} name="scan_gap" value={params.scan_gap} min="0.01" max="1" step="0.01" colorCls="text-blue-300" />
        </div>
      </div>
    </div>
  );
};

export default ParamControls;
