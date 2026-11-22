// Shared look-and-feel helpers for the app, matching the public (server-rendered) pages.

// Unit colors come from the API (backend/public.py UNIT_THEME); this is the fallback.
const FALLBACK_UNIT = { color: '#7fd3e6', text: '#111', light: '#7fd3e6' }

// Inline CSS variables used by .unit-bg / .unit-text / .unit-border / .unit-ring
export const unitStyle = (unit) => {
    const u = unit || FALLBACK_UNIT
    return { '--unit': u.color || FALLBACK_UNIT.color, '--unit-text': u.text || '#111', '--unit-light': u.light || u.color || FALLBACK_UNIT.light }
}

// Chapter quiz grade colors: green / yellow / pink
export const gradeColor = (grade) => grade >= 85 ? '#C6E83A' : grade >= 60 ? '#FFC93C' : '#FF6FAE'

// Topic mastery status colors and labels (backend/mastery.py statuses)
export const MASTERY = {
    mastered: { color: '#C6E83A', label: 'Mastered' },
    getting_there: { color: '#FFC93C', label: 'Getting there' },
    needs_work: { color: '#FF8A3D', label: 'Needs work' },
}

// The joke levels used across the app
export const masteryJoke = (percent) => {
    if (percent === null || percent === undefined) return 'Not yet started'
    if (percent > 80) return 'Econo-ninja-level'
    if (percent > 70) return 'Fiscal Phenom'
    if (percent > 60) return 'Curve Whisperer'
    if (percent > 50) return 'Sort of Chart Challenged'
    if (percent > 0) return 'A bit Econ-fused'
    return 'Not yet started'
}

// "1.5 Absolute and Comparative Advantage" -> ["1.5", "Absolute and Comparative Advantage"]
export const splitChapterName = (name = '') => {
    const [num, ...rest] = name.split(' ')
    return rest.length ? [num, rest.join(' ')] : ['', name]
}

// Public video page (full page load; it's server-rendered)
export const videoPageUrl = (chapter) => chapter?.slug ? `/videos/${encodeURIComponent(chapter.slug)}` : '/videos'
export const goToVideoPage = (chapter) => window.location.assign(videoPageUrl(chapter))
export const goToLibrary = () => window.location.assign('/videos')

export const thumbUrl = (chapter, size = 'hqdefault') => chapter?.yt ? `https://i.ytimg.com/vi/${chapter.yt}/${size}.jpg` : null
