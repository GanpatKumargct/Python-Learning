import React, { createContext, useContext, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

const FormContext = createContext(undefined);

export const FormProvider = ({ children }) => {
  const [title, setTitle] = useState('Untitled Form');
  const [description, setDescription] = useState('');
  const [schema, setSchema] = useState({
    pages: [{ id: 'page-1', title: 'Page 1', fields: [] }]
  });
  const [selectedFieldId, setSelectedFieldId] = useState(null);
  const [activePageId, setActivePageId] = useState('page-1');

  const addPage = () => {
    const newPage = { id: `page-${uuidv4()}`, title: `Page ${schema.pages.length + 1}`, fields: [] };
    setSchema(prev => ({ ...prev, pages: [...prev.pages, newPage] }));
    setActivePageId(newPage.id);
  };

  const addField = (pageId, type) => {
    const newField = {
      id: `field-${uuidv4()}`,
      type,
      label: `New ${type} field`,
      required: false,
    };
    if (['select', 'radio', 'checkbox'].includes(type)) {
      newField.options = ['Option 1', 'Option 2'];
    }

    setSchema(prev => {
      const pages = prev.pages.map(p => {
        if (p.id === pageId) {
          return { ...p, fields: [...p.fields, newField] };
        }
        return p;
      });
      return { ...prev, pages };
    });
    setSelectedFieldId(newField.id);
  };

  const updateField = (pageId, fieldId, updates) => {
    setSchema(prev => {
      const pages = prev.pages.map(p => {
        if (p.id === pageId) {
          return {
            ...p,
            fields: p.fields.map(f => f.id === fieldId ? { ...f, ...updates } : f)
          };
        }
        return p;
      });
      return { ...prev, pages };
    });
  };

  const removeField = (pageId, fieldId) => {
    setSchema(prev => {
      const pages = prev.pages.map(p => {
        if (p.id === pageId) {
          return {
            ...p,
            fields: p.fields.filter(f => f.id !== fieldId)
          };
        }
        return p;
      });
      return { ...prev, pages };
    });
    if (selectedFieldId === fieldId) {
      setSelectedFieldId(null);
    }
  };

  const value = {
    title,
    setTitle,
    description,
    setDescription,
    schema,
    addPage,
    activePageId,
    setActivePage: setActivePageId,
    selectedFieldId,
    selectField: setSelectedFieldId,
    addField,
    updateField,
    removeField
  };

  return <FormContext.Provider value={value}>{children}</FormContext.Provider>;
};

export const useFormContext = () => {
  const context = useContext(FormContext);
  if (context === undefined) {
    throw new Error('useFormContext must be used within a FormProvider');
  }
  return context;
};
