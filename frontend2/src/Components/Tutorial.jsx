import { useEffect, useLayoutEffect, useState } from "react"

// The dashboard tour shown after signing up. Each step spotlights an element marked data-tour="...".
const STEPS = [
    {
        target: null,
        title: 'Welcome to your dashboard!',
        body: <>
            <p>Give us a quick second to walk you through the page. We know, we know, you’ve been on a million websites before. You're basically the internet whisperer. But humor us, alright? This is <em>your</em> dashboard, where you can review your progress, videos watched, quiz scores and topic mastery. No judgment here... okay, maybe just a little.</p>
            <p>We’ll try to keep the jargon and cringe to a minimum. Ready? Cool, let’s do this thing!</p>
        </>,
        next: 'Next stop: enlightenment',
        skip: 'Skip the awkward tour',
    },
    {
        target: 'upnext',
        title: 'Up next',
        body: <p>Your personal cheerleader, telling you what chapter you're currently <i>surviving</i>. Whether you're about to watch another mind-blowing video or dive into a quiz, this is your trusty guide. Click it and boom: on to your next step toward total mastery (or at least faking it till you make it)!</p>,
        next: 'Keep the magic going!',
        skip: 'Boring. No more.',
    },
    {
        target: 'plan',
        title: 'Your study plan',
        body: <p>Your grand master plan... or as we like to call it, 'organized chaos.' Every unit lives here, with a tracker showing how much you’ve actually done. Click a chapter to open it: you’ll see whether you watched the video, your quiz grade, and how well you’ve mastered each topic (our algorithm tries its best!).</p>,
        next: 'Amazing! More!',
        skip: "I'm out.",
    },
    {
        target: 'practice',
        title: 'Practice',
        body: <p>Need more practice? The Gauntlet goes straight for your weak spots, or you can hand-craft a quiz by picking topics. Show those questions who’s boss!</p>,
        next: 'One more',
        skip: 'Enough talk.',
    },
    {
        target: 'menu',
        title: 'Your menu',
        body: <p>You can teleport out of this Econo-wasteland to any other part of the site from your menu: the video library, review quizzes, your study plan, and logging out.</p>,
        next: "Enough talk. Let's go.",
        skip: null,
    },
]

const PAD = 8

export const Tutorial = ({ showModal }) => {
    const [step, setStep] = useState(showModal ? 0 : null)
    const [rect, setRect] = useState(null)
    const current = step === null ? null : STEPS[step]

    useEffect(() => {
        if (showModal) {
            setStep(0)
            try { localStorage.setItem('hasVisitedDashboard', 'true') } catch (e) { /* private mode */ }
        }
    }, [showModal])

    // Find the spotlighted element, bring it into view, and track where it is
    useLayoutEffect(() => {
        if (!current?.target) { setRect(null); return }
        const el = document.querySelector(`[data-tour="${current.target}"]`)
        if (!el) { setRect(null); return }
        el.scrollIntoView({ block: 'center' })
        const measure = () => setRect(el.getBoundingClientRect())
        measure()
        window.addEventListener('resize', measure)
        window.addEventListener('scroll', measure, true)
        return () => {
            window.removeEventListener('resize', measure)
            window.removeEventListener('scroll', measure, true)
        }
    }, [current])

    if (!current) return null
    const close = () => setStep(null)
    const isLast = step === STEPS.length - 1

    // Bubble below the spotlight if there's room, otherwise above; centered when there's no target
    let bubbleStyle = { left: '50%', top: '50%', transform: 'translate(-50%, -50%)' }
    if (rect && rect.height > window.innerHeight * 0.55) {
        // Tall section (e.g. a long study plan): keep the bubble pinned at the bottom of the screen
        bubbleStyle = { right: 16, bottom: 16 }
    } else if (rect) {
        const below = rect.bottom + PAD + 16
        const left = Math.min(Math.max(16, rect.left), window.innerWidth - 400)
        bubbleStyle = below + 260 < window.innerHeight
            ? { left, top: below }
            : { left, bottom: window.innerHeight - rect.top + PAD + 16 }
    }

    return (
        <div className="fixed inset-0 z-[70]" role="dialog" aria-modal="true" aria-label={current.title}>
            {rect
                ? <div className="fixed rounded-2xl ring-4 ring-[#FFC93C] pointer-events-none transition-all"
                    style={{ left: rect.left - PAD, top: rect.top - PAD, width: rect.width + PAD * 2, height: rect.height + PAD * 2, boxShadow: '0 0 0 9999px rgba(0,0,0,.65)' }}></div>
                : <div className="fixed inset-0 bg-black/65"></div>}
            <div className="fixed w-[min(24rem,calc(100vw-2rem))] panel border border-white/15 rounded-2xl shadow-2xl p-5" style={bubbleStyle}>
                <p className="text-xs uppercase tracking-widest font-bold text-[#7fd3e6]">Tour · {step + 1} of {STEPS.length}</p>
                <h2 className="mt-1 text-xl font-extrabold">{current.title}</h2>
                <div className="mt-2 space-y-2 text-sm text-gray-200">{current.body}</div>
                <div className="mt-4 flex flex-wrap gap-2">
                    <button type="button" className="btn-primary px-4 py-2 text-sm" onClick={() => (isLast ? close() : setStep(step + 1))}>{current.next}</button>
                    {current.skip && <button type="button" className="btn-secondary px-4 py-1.5 text-sm" onClick={close}>{current.skip}</button>}
                </div>
            </div>
        </div>
    )
}
