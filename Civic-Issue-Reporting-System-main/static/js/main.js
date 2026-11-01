window.refreshCaptcha = function(formType) {
    const imgId = formType === "login" ? "loginCaptchaImg" : "registerCaptchaImg";
    const img = document.getElementById(imgId);
    if (img) {
        img.src = "/captcha/" + formType + "?t=" + new Date().getTime();
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("imageInput");
    const preview = document.getElementById("imagePreview");
    const aiContainer = document.getElementById("aiDetectorContainer");
    const aiScanning = document.getElementById("aiScanningState");
    const aiResultCard = document.getElementById("aiResultCard");
    const aiBadgeIcon = document.getElementById("aiBadgeIcon");
    const aiBadgeText = document.getElementById("aiBadgeText");
    const aiBadgeConfidence = document.getElementById("aiBadgeConfidence");
    const aiBadgeReason = document.getElementById("aiBadgeReason");
    const aiBadgeTags = document.getElementById("aiBadgeTags");
    const categorySelect = document.querySelector('select[name="category"]');

    if (input && preview) {
        function runAIDetection(file) {
            if (!aiContainer || !aiScanning || !aiResultCard) return;

            aiContainer.style.display = "block";
            aiScanning.style.display = "flex";
            aiResultCard.style.display = "none";
            const bboxOverlay = document.getElementById("bboxOverlay");
            if (bboxOverlay) bboxOverlay.innerHTML = "";

            const formData = new FormData();
            formData.append("image", file);

            const descEl = document.querySelector('textarea[name="description"]');
            if (descEl && descEl.value.trim()) {
                formData.append("description", descEl.value.trim());
            }
            if (categorySelect && categorySelect.value) {
                formData.append("category", categorySelect.value);
            }

            fetch("/api/ai-detect-image", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                aiScanning.style.display = "none";
                if (!data.success) {
                    aiContainer.style.display = "none";
                    return;
                }

                aiResultCard.style.display = "block";
                aiResultCard.classList.remove("ai-verified", "ai-flagged", "ai-review");

                const decisionPill = document.getElementById("aiDecisionPill");
                const detectedCatText = document.getElementById("aiDetectedCategoryText");
                const textMatchTag = document.getElementById("aiTextMatchTag");

                const decision = (data.decision || (data.is_issue ? "ACCEPT" : "REJECT")).toUpperCase();

                if (decision === "ACCEPT") {
                    aiResultCard.classList.add("ai-verified");
                    if (decisionPill) {
                        decisionPill.className = "ai-decision-pill accept";
                        decisionPill.textContent = "ACCEPT";
                    }
                    if (aiBadgeIcon) aiBadgeIcon.textContent = "✅";
                    if (aiBadgeText) aiBadgeText.textContent = "AI Verified: Genuine Civic Issue";
                } else if (decision === "MANUAL_REVIEW") {
                    aiResultCard.classList.add("ai-review");
                    if (decisionPill) {
                        decisionPill.className = "ai-decision-pill manual-review";
                        decisionPill.textContent = "MANUAL REVIEW";
                    }
                    if (aiBadgeIcon) aiBadgeIcon.textContent = "⚠️";
                    if (aiBadgeText) aiBadgeText.textContent = "Queued for Manual Admin Review";
                } else {
                    aiResultCard.classList.add("ai-flagged");
                    if (decisionPill) {
                        decisionPill.className = "ai-decision-pill reject";
                        decisionPill.textContent = "REJECT";
                    }
                    if (aiBadgeIcon) aiBadgeIcon.textContent = "❌";
                    if (aiBadgeText) aiBadgeText.textContent = "Validation Failed: Rejected";
                }

                if (aiBadgeConfidence) {
                    aiBadgeConfidence.textContent = `${Math.round(data.confidence || 0)}% Confidence`;
                }

                // Detected category & Text match
                if (detectedCatText) {
                    detectedCatText.textContent = data.category || "Unspecified";
                }
                if (textMatchTag) {
                    if (data.text_analysis && data.text_analysis.is_available) {
                        textMatchTag.style.display = "inline-block";
                        if (data.is_mismatch) {
                            textMatchTag.style.background = "#FEE2E2";
                            textMatchTag.style.color = "#991B1B";
                            textMatchTag.textContent = `⚠️ Text Mismatch: Predicted ${data.text_analysis.predicted_issue_type}`;
                        } else {
                            textMatchTag.style.background = "#E0F2FE";
                            textMatchTag.style.color = "#0369A1";
                            textMatchTag.textContent = `✓ Text Match: ${data.text_analysis.predicted_issue_type}`;
                        }
                    } else {
                        textMatchTag.style.display = "none";
                    }
                }

                // Auto-suggest category if user hasn't selected one
                if (categorySelect && (!categorySelect.value || categorySelect.value === "") && data.category && data.category !== "Other" && data.category !== "Non-Civic / Irrelevant") {
                    for (let opt of categorySelect.options) {
                        if (opt.value === data.category) {
                            categorySelect.value = data.category;
                            break;
                        }
                    }
                }

                if (aiBadgeReason) {
                    aiBadgeReason.innerHTML = data.reason || data.explanation || "";
                }

                // Render detail tags
                if (aiBadgeTags) {
                    aiBadgeTags.innerHTML = "";
                    if (data.category && data.category !== "Other" && data.category !== "Non-Civic / Irrelevant") {
                        const catTag = document.createElement("span");
                        catTag.className = "ai-tag";
                        catTag.textContent = `🏷️ ${data.category}`;
                        aiBadgeTags.appendChild(catTag);
                    }

                    // Sharpness tag
                    if (typeof data.blur_score === "number") {
                        const blurTag = document.createElement("span");
                        blurTag.className = "ai-tag";
                        blurTag.textContent = data.is_blurry ? `⚠️ Blurry (${data.blur_score})` : `🔍 Sharpness: ${data.blur_score}`;
                        aiBadgeTags.appendChild(blurTag);
                    }

                    // Duplicate tag
                    const dupTag = document.createElement("span");
                    dupTag.className = "ai-tag";
                    dupTag.textContent = data.is_duplicate ? "⚠️ Potential Duplicate" : "✓ Unique Photo";
                    aiBadgeTags.appendChild(dupTag);

                    // AI generated check
                    const genTag = document.createElement("span");
                    genTag.className = "ai-tag";
                    genTag.textContent = data.is_ai_generated ? "🤖 Synthetic / AI-Generated" : "📷 Camera Authenticity Confirmed";
                    aiBadgeTags.appendChild(genTag);

                    const engTag = document.createElement("span");
                    engTag.className = "ai-tag ai-engine";
                    engTag.textContent = "🤖 Multi-Modal Triage Engine";
                    aiBadgeTags.appendChild(engTag);
                }

                // Render localized bounding boxes
                if (bboxOverlay && Array.isArray(data.boxes)) {
                    bboxOverlay.innerHTML = "";
                    data.boxes.forEach(box => {
                        if (box.box_norm && box.box_norm.length === 4) {
                            const [x1, y1, x2, y2] = box.box_norm;
                            const boxEl = document.createElement("div");
                            boxEl.className = `ai-bbox ${box.class || ""}`;
                            boxEl.style.left = `${(x1 * 100).toFixed(2)}%`;
                            boxEl.style.top = `${(y1 * 100).toFixed(2)}%`;
                            boxEl.style.width = `${((x2 - x1) * 100).toFixed(2)}%`;
                            boxEl.style.height = `${((y2 - y1) * 100).toFixed(2)}%`;

                            const labelEl = document.createElement("span");
                            labelEl.className = "ai-bbox-label";
                            const confPct = Math.round((box.confidence || 0.95) * 100);
                            labelEl.textContent = `${box.label || box.class} (${confPct}%)`;
                            boxEl.appendChild(labelEl);

                            bboxOverlay.appendChild(boxEl);
                        }
                    });
                }
            })
            .catch(err => {
                console.error("AI detector error:", err);
                if (aiScanning) aiScanning.style.display = "none";
                if (aiContainer) aiContainer.style.display = "none";
            });
        }

        input.addEventListener("change", function () {
            const file = this.files[0];
            const bboxOverlay = document.getElementById("bboxOverlay");
            if (!file) {
                preview.style.display = "none";
                if (bboxOverlay) bboxOverlay.innerHTML = "";
                if (aiContainer) aiContainer.style.display = "none";
                return;
            }
            if (file.size > 5 * 1024 * 1024) {
                alert("Image size must be less than 5 MB.");
                this.value = "";
                preview.style.display = "none";
                if (bboxOverlay) bboxOverlay.innerHTML = "";
                if (aiContainer) aiContainer.style.display = "none";
                return;
            }
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";

            runAIDetection(file);
        });

        // Retry / Clear Button handler
        const retryBtn = document.getElementById("aiRetryBtn");
        if (retryBtn) {
            retryBtn.addEventListener("click", function () {
                input.value = "";
                preview.src = "";
                preview.style.display = "none";
                const bboxOverlay = document.getElementById("bboxOverlay");
                if (bboxOverlay) bboxOverlay.innerHTML = "";
                if (aiContainer) aiContainer.style.display = "none";
            });
        }
    }


    setTimeout(() => {
        document.querySelectorAll(".flash").forEach(el => {
            el.style.opacity = "0";
            el.style.transition = "opacity .5s";
            setTimeout(() => el.remove(), 500);
        });
    }, 4000);

    // Mobile Navbar Toggle for Homepage
    const mobileToggle = document.getElementById("crMobileToggle");
    const navMenu = document.getElementById("crNavMenu");

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener("click", function () {
            navMenu.classList.toggle("open");
        });

        // Close mobile menu when clicking outside or on a link
        document.querySelectorAll(".cr-nav-item a, .cr-mobile-auth a").forEach(link => {
            link.addEventListener("click", function () {
                navMenu.classList.remove("open");
            });
        });
    }

    // Smooth Scroll for in-page anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId && targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});
