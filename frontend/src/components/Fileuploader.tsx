import { Dialog } from "primereact/dialog";
import { FileUpload } from "primereact/fileupload";
import type { Toast } from "primereact/toast";

export default function Fileuploader({
  visible,
  setVisible,
  setFileupload,
  toast,
}: {
  visible: boolean;
  setVisible: React.Dispatch<React.SetStateAction<boolean>>;
  setFileupload: React.Dispatch<React.SetStateAction<string | null>>;
  toast: React.RefObject<Toast | null>;
}) {
  return (
    <Dialog
      header="Header"
      visible={visible}
      style={{ width: "50vw" }}
      onHide={() => {
        if (!visible) return;
        setVisible(false);
      }}
    >
      <p className="m-0">
        <FileUpload
          name="file"
          accept="text/csv"
          url="http://127.0.0.1:8000/upload"
          mode="advanced"
          onUpload={(data) => {
            toast.current?.show({
              severity: "info",
              summary: "File Uploaded Successfully",
              detail: "File Uploaded Successfully",
            });
            setVisible(false);
            setFileupload(JSON.parse(data.xhr.response).location);
          }}
        />
      </p>
    </Dialog>
  );
}
