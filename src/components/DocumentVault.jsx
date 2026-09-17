import { useEffect, useRef, useState } from 'react';
import { documentsAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

const MAX_FILE_BYTES = 10 * 1024 * 1024; // keep in sync with backend limit

export default function DocumentVault() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await documentsAPI.list();
      setDocs((res && res.data) || []);
    } catch (err) {
      setError(err.message || 'Could not load documents.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleFileChange = async (e) => {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    setError('');

    if (file.size > MAX_FILE_BYTES) {
      setError('That file is too large (max 10MB).');
      e.target.value = '';
      return;
    }

    setUploading(true);
    try {
      await documentsAPI.upload(file);
      await load();
    } catch (err) {
      setError(err.message || 'Upload failed. Try a different file.');
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const handleDelete = async (docId) => {
    setError('');
    try {
      await documentsAPI.remove(docId);
      setDocs((prev) => prev.filter((d) => d.id !== docId));
    } catch (err) {
      setError(err.message || 'Could not delete this document.');
    }
  };

  return (
    <div className="safety-card">
      <h2>Document Vault</h2>
      <p className="desc">Store important documents privately. Not encrypted at rest in this prototype.</p>

      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
        disabled={uploading}
        style={{ marginBottom: 12 }}
      />
      {uploading && <Loading label="Uploading…" />}
      <ErrorMessage message={error} />

      {loading ? (
        <Loading label="Loading documents…" />
      ) : docs.length === 0 ? (
        <p className="state-line">No documents saved yet.</p>
      ) : (
        <div>
          {docs.map((doc) => (
            <div key={doc.id} className="doc-row">
              <span>{doc.filename}</span>
              <div className="doc-row-actions">
                <a href={documentsAPI.downloadUrl(doc.id)} target="_blank" rel="noreferrer">
                  Download
                </a>
                <button className="danger" onClick={() => handleDelete(doc.id)}>
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
