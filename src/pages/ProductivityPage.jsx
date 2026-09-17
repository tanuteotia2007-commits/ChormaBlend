import Header from '../components/Header';
import Notes from '../components/Notes';
import Todo from '../components/Todo';
import Planner from '../components/Planner';

export default function ProductivityPage({ onUnlocked }) {
  const today = new Date();

  const dateLabel = today.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="workspace-page">
      <Header onUnlocked={onUnlocked} />

      <main className="workspace-body">
        <section className="workspace-intro">
          <div>
            <span className="eyebrow">YOUR WORKSPACE</span>
            <h1>Welcome back!</h1>
            <p>Keep your thoughts, tasks and plans in one quiet place.</p>
          </div>

          <div className="today-pill">
            <span className="today-dot" />
            {dateLabel}
          </div>
        </section>

        <section className="workspace-grid">
          <Notes />
          <Todo />
          <Planner />
        </section>

        <footer className="workspace-footer">
          <span>Chroma Blend</span>
          <span>Everything in one place.</span>
        </footer>
      </main>
    </div>
  );
}