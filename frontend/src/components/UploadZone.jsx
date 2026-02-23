import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud } from 'lucide-react';
import { useTranslation } from 'react-i18next';

const UploadZone = ({ onFileSelected, isLoading }) => {
  const { t } = useTranslation();

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      onFileSelected(acceptedFiles[0]);
    }
  }, [onFileSelected]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'image/svg+xml': ['.svg']
    },
    maxFiles: 1,
    disabled: isLoading
  });

  return (
    <div 
      {...getRootProps()} 
      className={`
        relative overflow-hidden w-full p-10 border-2 border-dashed rounded-2xl cursor-pointer 
        transition-all duration-300 ease-out group
        ${isDragActive ? 'border-blue-500 bg-blue-500/10 scale-[1.02]' : 'border-gray-700 hover:border-blue-400 bg-gray-800/50 hover:bg-gray-800'}
        ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
      `}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center space-y-4 text-center">
        <div className={`p-4 rounded-full transition-colors duration-300 ${isDragActive ? 'bg-blue-500/20' : 'bg-gray-700/50 group-hover:bg-blue-500/20'}`}>
          <UploadCloud className={`w-12 h-12 transition-colors duration-300 ${isDragActive ? 'text-blue-400' : 'text-gray-400 group-hover:text-blue-400'}`} />
        </div>
        
        {isLoading ? (
          <h3 className="text-xl font-semibold text-blue-400 animate-pulse">{t('uploading')}</h3>
        ) : (
          <div>
            <h3 className="text-xl font-semibold text-gray-200">
              {acceptedFiles.length > 0 ? acceptedFiles[0].name : t('drag_drop')}
            </h3>
            <p className="text-gray-500 mt-2">{t('click_to_browse')}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadZone;
