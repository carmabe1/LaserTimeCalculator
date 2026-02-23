import React from 'react';
import { useTranslation } from 'react-i18next';
import { Clock, Layers, Maximize } from 'lucide-react';

const ResultsDashboard = ({ report }) => {
  const { t } = useTranslation();

  if (!report) return null;

  const {
    formatted_time,
    total_distance_burned_mm,
    total_distance_transit_mm,
    layer_breakdown
  } = report;

  const formatSecs = (secs) => {
    if (!secs) return '0.0s';
    return `${secs.toFixed(1)}s`;
  };

  const LayerRow = ({ label, time, distance, area, colorClass, isBg }) => (
    <div className={`p-4 rounded-xl border border-gray-800 flex justify-between items-center ${isBg ? 'bg-gray-800/30' : ''}`}>
      <div className="flex items-center space-x-3">
        <div className={`w-3 h-3 rounded-full ${colorClass}`}></div>
        <span className="font-medium text-gray-300">{label}</span>
      </div>
      <div className="text-right">
        <span className="text-lg font-bold text-gray-100 block">{formatSecs(time)}</span>
        {distance > 0 && <span className="text-xs text-gray-500">{t('distance')} {distance.toFixed(1)}mm</span>}
        {area > 0 && <span className="text-xs text-gray-500">{t('area')} {area.toFixed(1)}mm²</span>}
      </div>
    </div>
  );

  return (
    <div className="bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-gray-700">
      <div className="bg-gray-900 p-8 flex flex-col items-center justify-center border-b border-gray-700">
        <Clock className="w-12 h-12 text-blue-500 mb-4 animate-pulse" />
        <h2 className="text-lg text-gray-400 font-medium mb-1">{t('total_time')}</h2>
        <div className="text-5xl font-mono font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400 drop-shadow-sm">
          {formatted_time}
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-lg font-semibold flex items-center space-x-2 text-gray-200 mb-4">
          <Layers className="w-5 h-5 text-gray-400" />
          <span>{t('layer_breakdown')}</span>
        </h3>
        <div className="grid gap-3">
          <LayerRow 
            label={t('cut')} 
            time={layer_breakdown.cut.time} 
            distance={layer_breakdown.cut.distance} 
            colorClass="bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]" 
            isBg
          />
          <LayerRow 
            label={t('mark')} 
            time={layer_breakdown.mark.time} 
            distance={layer_breakdown.mark.distance} 
            colorClass="bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]" 
          />
          <LayerRow 
            label={t('raster')} 
            time={layer_breakdown.raster.time} 
            area={layer_breakdown.raster.area} 
            colorClass="bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" 
            isBg
          />
          <LayerRow 
            label={t('transit')} 
            time={report.transit_time_seconds} 
            distance={total_distance_transit_mm} 
            colorClass="bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]" 
          />
        </div>

        <div className="mt-8 text-center bg-gray-900/50 p-4 rounded-xl border border-gray-800">
          <p className="text-sm text-gray-400 mb-2">{t('feedback_prompt')}</p>
          <a href="mailto:pruebasdealgo@gmail.com" className="text-blue-400 hover:text-blue-300 font-medium transition-colors">
            {t('feedback_link')}
          </a>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;
