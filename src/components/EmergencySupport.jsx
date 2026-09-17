import { useEffect, useState } from 'react';
import { contactsAPI, emergencyAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

export default function EmergencySupport() {
  const [contacts, setContacts] = useState([]);
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [relationship, setRelationship] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const [confirmingSOS, setConfirmingSOS] = useState(false);
  const [sendingSOS, setSendingSOS] = useState(false);
  const [sosResult, setSosResult] = useState(null);

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await contactsAPI.list();
      setContacts((res && res.data) || []);
    } catch (err) {
      setError(err.message || 'Could not load contacts.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleAddContact = async (e) => {
    e.preventDefault();
    if (!name.trim() || !phone.trim()) {
      setError('Name and phone number are required.');
      return;
    }
    setSaving(true);
    setError('');
    try {
      await contactsAPI.add({ name: name.trim(), phone: phone.trim(), relationship: relationship.trim() });
      setName('');
      setPhone('');
      setRelationship('');
      await load();
    } catch (err) {
      setError(err.message || 'Could not save this contact.');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteContact = async (contactId) => {
    setError('');
    try {
      await contactsAPI.remove(contactId);
      setContacts((prev) => prev.filter((c) => c.id !== contactId));
      setSelectedIds((prev) => prev.filter((id) => id !== contactId));
    } catch (err) {
      setError(err.message || 'Could not delete this contact.');
    }
  };

  const toggleSelected = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleSendSOS = async () => {
    setSendingSOS(true);
    setError('');
    setSosResult(null);
    try {
      const res = await emergencyAPI.sendSOS(selectedIds);
      setSosResult(res);
    } catch (err) {
      setError(err.message || 'Could not send the SOS request.');
    } finally {
      setSendingSOS(false);
      setConfirmingSOS(false);
    }
  };

  return (
    <div className="safety-card">
      <h2>Emergency Support</h2>
      <p className="desc">Trusted contacts and a one-tap SOS.</p>

      <form onSubmit={handleAddContact}>
        <input
          className="safety-input"
          type="text"
          placeholder="Contact name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          disabled={saving}
        />
        <input
          className="safety-input"
          type="tel"
          placeholder="Phone number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          disabled={saving}
        />
        <input
          className="safety-input"
          type="text"
          placeholder="Relationship (optional)"
          value={relationship}
          onChange={(e) => setRelationship(e.target.value)}
          disabled={saving}
        />
        <button className="btn-accent" type="submit" disabled={saving || !name.trim() || !phone.trim()}>
          {saving ? 'Saving…' : 'Add contact'}
        </button>
      </form>

      <ErrorMessage message={error} />

      {loading ? (
        <Loading label="Loading contacts…" />
      ) : contacts.length === 0 ? (
        <p className="state-line">No trusted contacts saved yet.</p>
      ) : (
        <div style={{ margin: '16px 0' }}>
          {contacts.map((c) => (
            <div key={c.id} className="contact-row">
              <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(c.id)}
                  onChange={() => toggleSelected(c.id)}
                />
                {c.name} — {c.phone}
                {c.relationship ? ` (${c.relationship})` : ''}
              </label>
              <div className="contact-row-actions">
                <button className="danger" onClick={() => handleDeleteContact(c.id)}>
                  Remove
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {!confirmingSOS ? (
        <button
          className="btn-danger"
          onClick={() => setConfirmingSOS(true)}
          disabled={contacts.length === 0}
        >
          Send SOS
        </button>
      ) : (
        <div>
          <p className="desc">
            This will notify {selectedIds.length > 0 ? selectedIds.length : 'all'} selected contact(s). Confirm?
          </p>
          <button className="btn-danger" onClick={handleSendSOS} disabled={sendingSOS} style={{ marginRight: 8 }}>
            {sendingSOS ? 'Sending…' : 'Yes, send now'}
          </button>
          <button className="btn-quiet" onClick={() => setConfirmingSOS(false)} disabled={sendingSOS}>
            Cancel
          </button>
        </div>
      )}

      {sosResult && (
        <p className="state-line" style={{ marginTop: 12 }}>
          {sosResult.success
            ? sosResult.message || 'SOS request recorded.'
            : sosResult.message || 'SOS request failed.'}
        </p>
      )}
    </div>
  );
}
