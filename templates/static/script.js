document.addEventListener('DOMContentLoaded', function() {
    console.log('🎲 YT BoardGame Static cargado correctamente');
    
    // Animación de entrada para las tarjetas
    const cards = document.querySelectorAll('.channel-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Expandir/colapsar videos al hacer clic
    const videoLists = document.querySelectorAll('.videos-list');
    videoLists.forEach(list => {
        const videos = Array.from(list.querySelectorAll('.video-item'));
        const fullCount = parseInt(list.dataset.fullCount, 10);
        const initialShowCount = 3; // Mostrar los primeros 3 videos por defecto

        if (videos.length > initialShowCount) {
            // Ocultar videos extra
            for (let i = initialShowCount; i < videos.length; i++) {
                videos[i].style.display = 'none';
            }
            
            const toggleBtn = document.createElement('div');
            toggleBtn.className = 'video-toggle-btn';
            toggleBtn.textContent = `📖 Ver los ${fullCount} videos completos`;
            
            let expanded = false;
            toggleBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevenir que el clic en el botón active el enlace del canal
                e.stopPropagation(); // Detener la propagación para evitar activar el enlace del canal
                
                expanded = !expanded;
                for (let i = initialShowCount; i < videos.length; i++) {
                    videos[i].style.display = expanded ? 'flex' : 'none'; // 'flex' porque el estilo CSS lo usa
                }
                toggleBtn.textContent = expanded ? `📖 Ocultar videos` : `📖 Ver los ${fullCount} videos completos`;
            });
            
            list.parentNode.appendChild(toggleBtn); // Añadir el botón después del videos-list dentro de channel-card
        } else if (videos.length === 0) {
            // Si no hay videos, se muestra un mensaje "No hay videos recientes disponibles."
            // y no se crea ningún botón de "Ver más".
            const noVideosMessage = document.createElement('div');
            noVideosMessage.className = 'no-videos-message';
            noVideosMessage.textContent = 'No hay videos recientes disponibles.';
            list.appendChild(noVideosMessage);
        }
    });
});