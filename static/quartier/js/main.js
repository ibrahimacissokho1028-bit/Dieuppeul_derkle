(() => {
    const header = document.querySelector(".site-header");
    const menuButton = document.querySelector(".menu-toggle");
    const navigation = document.querySelector("#navigation-principale");

    const updateHeader = () => {
        if (header) header.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });

    if (menuButton && navigation) {
        menuButton.addEventListener("click", () => {
            const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
            menuButton.setAttribute("aria-expanded", String(!isExpanded));
            menuButton.setAttribute("aria-label", isExpanded ? "Ouvrir le menu" : "Fermer le menu");
            navigation.classList.toggle("is-open", !isExpanded);
        });
        navigation.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                menuButton.setAttribute("aria-expanded", "false");
                menuButton.setAttribute("aria-label", "Ouvrir le menu");
                navigation.classList.remove("is-open");
            });
        });
    }

    const revealElements = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        revealElements.forEach((element) => revealObserver.observe(element));
    } else {
        revealElements.forEach((element) => element.classList.add("is-visible"));
    }

    document.querySelectorAll(".filter-button").forEach((button) => {
        button.addEventListener("click", () => {
            const filter = button.dataset.filter;
            document.querySelectorAll(".filter-button").forEach((item) => {
                const active = item === button;
                item.classList.toggle("is-active", active);
                item.setAttribute("aria-pressed", String(active));
            });
            document.querySelectorAll(".gallery-item").forEach((photo) => {
                photo.classList.toggle("is-hidden", filter !== "all" && photo.dataset.category !== filter);
            });
        });
    });

    const slides = Array.from(document.querySelectorAll(".quote-card"));
    if (slides.length) {
        let currentSlide = 0;
        const currentLabel = document.querySelector("[data-carousel-current]");
        const showSlide = (nextIndex) => {
            currentSlide = (nextIndex + slides.length) % slides.length;
            slides.forEach((slide, index) => slide.classList.toggle("is-current", index === currentSlide));
            if (currentLabel) currentLabel.textContent = String(currentSlide + 1);
        };
        document.querySelector("[data-carousel-prev]")?.addEventListener("click", () => showSlide(currentSlide - 1));
        document.querySelector("[data-carousel-next]")?.addEventListener("click", () => showSlide(currentSlide + 1));
    }

    const counters = document.querySelectorAll("[data-count]");
    if ("IntersectionObserver" in window) {
        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                const element = entry.target;
                const target = Number(element.dataset.count);
                const duration = 1100;
                const startedAt = performance.now();
                const animate = (now) => {
                    const progress = Math.min((now - startedAt) / duration, 1);
                    element.textContent = Math.floor(target * (1 - (1 - progress) ** 3)).toLocaleString("fr-FR");
                    if (progress < 1) requestAnimationFrame(animate);
                };
                requestAnimationFrame(animate);
                observer.unobserve(element);
            });
        }, { threshold: 0.6 });
        counters.forEach((counter) => counterObserver.observe(counter));
    } else {
        counters.forEach((counter) => {
            counter.textContent = Number(counter.dataset.count).toLocaleString("fr-FR");
        });
    }
})();
