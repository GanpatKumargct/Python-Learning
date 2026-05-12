import { FormBuilder } from './modules/form-builder/FormBuilder';
import { FormProvider } from './context/FormContext';

function App() {
  return (
    <FormProvider>
      <FormBuilder />
    </FormProvider>
  );
}

export default App;
